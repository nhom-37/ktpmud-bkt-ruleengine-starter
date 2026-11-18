"""Rule Engine WAO/EAACI - khung bai tap BKT-1 (Track A), mon KTPMUD.

Sinh vien hien thuc ham classify() theo dac ta trong docs/decision-table.md.
KHONG tu dat nguong/quy tac moi chua co trong dac ta.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from typing import Optional, TypedDict
from uuid import uuid4


class PatientInput(TypedDict, total=False):
    """Input theo dung Data Dictionary trong docs/decision-table.md."""
    tuoi: float
    huyet_ap_tam_thu: Optional[int]
    huyet_ap_tam_thu_nen: Optional[int]
    co_di_nguyen_nghi_ngo: bool
    di_nguyen_qua_duong_hit: bool
    co_ton_thuong_da_niem_mac: bool
    co_trieu_chung_ho_hap: bool
    co_trieu_chung_tuan_hoan: bool
    co_trieu_chung_tieu_hoa_nang: bool


class ClassificationResult(TypedDict):
    muc_do: str  # "SOC_PHAN_VE" | "PHAN_VE" | "THEO_DOI" - dung dung nhan theo docs/decision-table.md
    rule_id: Optional[str]  # "R-SOC" | "R01-PV" | "R02-PV" | "R03-PV" | None
    ly_do: str


def _r01(patient: PatientInput) -> bool:
    return (
        patient.get("co_di_nguyen_nghi_ngo") is False
        and patient.get("co_ton_thuong_da_niem_mac") is True
        and (
            patient.get("co_trieu_chung_ho_hap") is True
            or patient.get("co_trieu_chung_tuan_hoan") is True
        )
    )


def _r02(patient: PatientInput) -> bool:
    systems = (
        "co_ton_thuong_da_niem_mac",
        "co_trieu_chung_ho_hap",
        "co_trieu_chung_tuan_hoan",
        "co_trieu_chung_tieu_hoa_nang",
    )
    return (
        patient.get("co_di_nguyen_nghi_ngo") is True
        and sum(patient.get(field) is True for field in systems) >= 2
    )


def _r03(patient: PatientInput) -> bool:
    return (
        patient.get("co_di_nguyen_nghi_ngo") is True
        and (
            patient.get("co_trieu_chung_tuan_hoan") is True
            or (
                patient.get("di_nguyen_qua_duong_hit") is False
                and patient.get("co_trieu_chung_ho_hap") is True
            )
        )
    )


_RULES = (("R01-PV", _r01), ("R02-PV", _r02), ("R03-PV", _r03))
_PRESSURE_FIELDS = {"huyet_ap_tam_thu", "huyet_ap_tam_thu_nen"}
_SESSION_UUID = str(uuid4())


def _valid_input(patient: PatientInput) -> bool:
    if not isinstance(patient, dict):
        return False
    for field, value in patient.items():
        if field not in PatientInput.__annotations__:
            return False
        if value is None:
            continue
        if field == "tuoi":
            if type(value) not in (int, float) or value < 0:
                return False
            if isinstance(value, float) and not math.isfinite(value):
                return False
        elif field in _PRESSURE_FIELDS:
            if type(value) is not int or value < 0:
                return False
        elif type(value) is not bool:
            return False
    return True


def _low_pressure(age: float, current: int, baseline: int | None) -> bool:
    if age < 1:
        return current < 70
    if age < 11:
        return current < 70 + 2 * age
    return current < 90 or (
        age >= 18 and baseline is not None and baseline > 0
        and 10 * current < 7 * baseline
    )


def _evaluate(patient: PatientInput) -> ClassificationResult:
    if not _valid_input(patient):
        return {"muc_do": "THEO_DOI", "rule_id": None, "ly_do": "Đầu vào không hợp lệ"}

    age = patient.get("tuoi")
    if age is None:
        return {"muc_do": "THEO_DOI", "rule_id": None, "ly_do": "Thiếu tuổi"}

    matched = next((code for code, rule in _RULES if rule(patient)), None)
    if matched is None:
        return {"muc_do": "THEO_DOI", "rule_id": None, "ly_do": "Chưa đủ dữ liệu để khớp quy tắc V1"}

    current = patient.get("huyet_ap_tam_thu")
    baseline = patient.get("huyet_ap_tam_thu_nen")
    if current is not None and _low_pressure(age, current, baseline):
        return {"muc_do": "SOC_PHAN_VE", "rule_id": "R-SOC", "ly_do": f"Khớp R-SOC dựa trên {matched}"}

    reason = f"Khớp {matched}"
    if current is None:
        reason += ". Thiếu huyết áp hiện tại để đánh giá sốc"
    elif age >= 18 and not baseline:
        reason += ". Chưa đủ dữ liệu huyết áp nền để tính mức giảm"
    return {"muc_do": "PHAN_VE", "rule_id": matched, "ly_do": reason}


def classify(patient: PatientInput) -> ClassificationResult:
    """Phân loại ca giả lập theo bảng V1 và ghi audit của phiên chạy."""
    result = _evaluate(patient)
    audit = {
        "Timestamp": datetime.now(timezone.utc).isoformat(),
        "User_UUID": _SESSION_UUID,
        "Action_Type": "CLASSIFY",
        "Status": result["muc_do"],
    }
    print(json.dumps(audit), file=sys.stderr)
    return result
