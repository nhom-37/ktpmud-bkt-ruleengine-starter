# Báo cáo kiểm thử · N37

Chạy ngày 18/11/2026 trên Windows, Python 3.13.13, GenuineIntel Family 6 Model 151. Lệnh `python -m unittest discover -s tests -v` cho kết quả **4 nhóm test đạt**, gồm các ca con về ưu tiên, ngưỡng, dữ liệu thiếu hoặc sai kiểu, định dạng audit và UUID của phiên. [Bộ test](https://github.com/nhom-37/ktpmud-bkt-ruleengine-starter)

`python benchmark.py` đo 3.000 lần sau 100 lần warm-up. Một lần chạy ghi nhận p50 0,0071 ms và p95 0,0109 ms, gồm tạo và ghi audit ra thiết bị rỗng. Các số liệu phản ánh môi trường đo cục bộ.

Máy dùng để kiểm tra hiện thiếu gói pytest. Kết quả `pytest -q` và GitHub Actions cần được xác nhận trên commit đã push.
