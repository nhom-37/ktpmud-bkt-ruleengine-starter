# N37 · Dr May Day Rule Engine

**educational/synthetic — not for clinical use**

Rule engine dùng bảng V1 để phân loại ca giả lập. Gọi `classify()` trong
`rule_engine.classifier` để nhận `muc_do`, `rule_id` và `ly_do`.

```powershell
python -m pip install -r requirements.txt
pytest -q
python benchmark.py
```

Có thể chạy bộ test bằng thư viện chuẩn với `python -m unittest discover -s tests -v`.
Audit được ghi ra stderr dưới dạng JSON từng dòng. Xem [ADR](DECISIONS.md).

Đặc tả theo [Bảng quyết định V1](docs/decision-table.md).
