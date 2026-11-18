"""Đo thời gian classify() trên dữ liệu giả lập, gồm ghi audit vào thiết bị rỗng."""
import os
import statistics
from contextlib import redirect_stderr
from time import perf_counter_ns

from rule_engine.classifier import classify


def main():
    reaction = {
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    }
    cases = ({}, reaction, dict(reaction, huyet_ap_tam_thu=80))
    samples = []
    with open(os.devnull, "w") as sink, redirect_stderr(sink):
        for index in range(100):
            classify(cases[index % len(cases)])
        for index in range(3000):
            case = cases[index % len(cases)]
            start = perf_counter_ns()
            classify(case)
            samples.append((perf_counter_ns() - start) / 1_000_000)
    print(f"n={len(samples)}, p50={statistics.median(samples):.4f} ms, "
          f"p95={statistics.quantiles(samples, n=100, method='inclusive')[94]:.4f} ms")


if __name__ == "__main__":
    main()
