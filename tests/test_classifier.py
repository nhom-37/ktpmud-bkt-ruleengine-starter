import io
import json
import unittest
from contextlib import redirect_stderr

from rule_engine.classifier import classify


CASE = {
    "tuoi": 25,
    "huyet_ap_tam_thu": 120,
    "huyet_ap_tam_thu_nen": 150,
    "co_di_nguyen_nghi_ngo": False,
    "co_ton_thuong_da_niem_mac": True,
    "co_trieu_chung_ho_hap": True,
    "co_trieu_chung_tuan_hoan": False,
    "co_trieu_chung_tieu_hoa_nang": False,
    "di_nguyen_qua_duong_hit": False,
}


class ClassifierTests(unittest.TestCase):
    def assert_case(self, case, level, rule_id):
        audit = io.StringIO()
        with redirect_stderr(audit):
            result = classify(case)
        self.assertEqual(set(result), {"muc_do", "rule_id", "ly_do"})
        self.assertEqual((result["muc_do"], result["rule_id"]), (level, rule_id))
        if rule_id:
            self.assertIn(rule_id, result["ly_do"])
        lines = audit.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines[0])
        self.assertEqual(set(record), {"Timestamp", "User_UUID", "Action_Type", "Status"})
        self.assertEqual(record["Status"], level)
        self.assertEqual(record["Action_Type"], "CLASSIFY")
        return record

    def test_rules_and_priority(self):
        self.assert_case(CASE, "PHAN_VE", "R01-PV")
        both = dict(CASE, co_di_nguyen_nghi_ngo=True)
        self.assert_case(both, "PHAN_VE", "R02-PV")
        r03 = dict(both, co_ton_thuong_da_niem_mac=False)
        self.assert_case(r03, "PHAN_VE", "R03-PV")
        inhaled = dict(r03, di_nguyen_qua_duong_hit=True)
        self.assert_case(inhaled, "THEO_DOI", None)
        self.assert_case(dict(inhaled, co_trieu_chung_tuan_hoan=True,
                              co_trieu_chung_ho_hap=False), "PHAN_VE", "R03-PV")
        self.assert_case(dict(both, huyet_ap_tam_thu=89), "SOC_PHAN_VE", "R-SOC")

    def test_boundaries(self):
        for age, pressure, baseline, shock in (
            (0.99, 69, None, True), (0.99, 70, None, False), (1, 70, None, True),
            (1, 72, None, False), (10.99, 90, None, True), (11, 90, None, False),
            (11, 89, None, True), (17.99, 100, 150, False), (18, 100, 150, True),
            (25, 104, 150, True), (25, 105, 150, False),
        ):
            with self.subTest(age=age, pressure=pressure):
                case = dict(CASE, tuoi=age, huyet_ap_tam_thu=pressure,
                            huyet_ap_tam_thu_nen=baseline)
                self.assert_case(case, "SOC_PHAN_VE" if shock else "PHAN_VE",
                                 "R-SOC" if shock else "R01-PV")

    def test_missing_values(self):
        for field, level, rule_id in (
            ("tuoi", "THEO_DOI", None),
            ("co_di_nguyen_nghi_ngo", "THEO_DOI", None),
            ("co_trieu_chung_tuan_hoan", "PHAN_VE", "R01-PV"),
            ("huyet_ap_tam_thu", "PHAN_VE", "R01-PV"),
            ("huyet_ap_tam_thu_nen", "PHAN_VE", "R01-PV"),
        ):
            with self.subTest(field=field):
                self.assert_case(dict(CASE, **{field: None}), level, rule_id)
                self.assert_case({key: value for key, value in CASE.items() if key != field},
                                 level, rule_id)
        self.assert_case(dict(CASE, huyet_ap_tam_thu=89, huyet_ap_tam_thu_nen=None),
                         "SOC_PHAN_VE", "R-SOC")

    def test_invalid_values_and_audit_session(self):
        session = self.assert_case(CASE, "PHAN_VE", "R01-PV")["User_UUID"]
        for case in (
            dict(CASE, tuoi=True), dict(CASE, tuoi=float("nan")), dict(CASE, tuoi=-1),
            dict(CASE, huyet_ap_tam_thu="80"), dict(CASE, huyet_ap_tam_thu=-1),
            dict(CASE, co_trieu_chung_ho_hap="false"), dict(CASE, unknown="synthetic"),
        ):
            record = self.assert_case(case, "THEO_DOI", None)
            self.assertEqual(record["User_UUID"], session)
