# Kế hoạch kiểm thử — Track A · Dr May Day

**Nhóm** N37 · **Mốc** Checkpoint 1, 08/11/2026

Đối chiếu test với mã A-01 đến A-11 và chính sách đầu vào của nhóm trong [REQUIREMENTS.md](REQUIREMENTS.md). Các ca sử dụng dữ liệu giả lập. Kết quả mong đợi dựa trên [bảng quyết định V1](https://raw.githubusercontent.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/bkt-2026-v1/docs/decision-table.md) và cách nhóm N37 áp dụng bảng.

## Dữ liệu cơ sở

Dùng bản ghi đầy đủ với `tuoi = 25.0`, `huyet_ap_tam_thu = 120`, `huyet_ap_tam_thu_nen = 150` và mọi cờ Boolean bằng `false`. Mỗi ca lấy một bản ghi riêng, sau đó thay các giá trị nêu trong bảng.

Trong bảng, “dị nguyên” là `co_di_nguyen_nghi_ngo`, “qua hít” là `di_nguyen_qua_duong_hit`. “Da”, “hô hấp”, “tuần hoàn” và “tiêu hóa” là các cờ triệu chứng tương ứng trong Data Dictionary. HATT là huyết áp tâm thu hiện tại.

## Ca thông thường và nhánh quy tắc

| Ca | Thay đổi so với bản ghi cơ sở | Kết quả mong đợi `muc_do` / `rule_id` |
| --- | --- | --- |
| N01 | Bật da và hô hấp. | `PHAN_VE` / `R01-PV` |
| N02 | Bật dị nguyên, da và tiêu hóa. | `PHAN_VE` / `R02-PV` |
| N03 | Bật dị nguyên và hô hấp. | `PHAN_VE` / `R03-PV` |
| N04 | Bật dị nguyên, qua hít và tuần hoàn. | `PHAN_VE` / `R03-PV` |
| N05 | Giữ nguyên bản ghi cơ sở. | `THEO_DOI` / `null` |
| N06 | Bật dị nguyên, qua hít và hô hấp. | `THEO_DOI` / `null` |
| N07 | HATT 80, giữ mọi cờ bằng `false`. | `THEO_DOI` / `null` |
| N08 | Bật da và tuần hoàn. | `PHAN_VE` / `R01-PV` |

## Ca sát ngưỡng và ưu tiên hai tầng

Giữ các cờ của N01 để ca luôn khớp R01. Khi đạt điều kiện sốc, mong đợi `SOC_PHAN_VE` / `R-SOC`. Với các giá trị còn lại trong bảng, mong đợi `PHAN_VE` / `R01-PV`.

| Ca | Tuổi | HATT đạt điều kiện sốc | HATT còn lại | HATT nền |
| --- | --- | --- | --- | --- |
| B01 | 0.5 | 69 | 70 | `null` |
| B02 | 1.0 | 71 | 72 | `null` |
| B03 | 10.5 | 90 | 91 | `null` |
| B04 | 11.0 | 89 | 90 | `null` |
| B05 | 17.99 | 89 | 90 | `null` |
| B06 | 18.0 | 89 | 90 | 100 |
| B07 | 25.0 | 104 | 105 và 106 | 150 |

B07 cô lập nhánh phần trăm vì cả ba giá trị HATT đều từ 90 trở lên. Giảm đúng 30% tại HATT 105 nằm ngoài điều kiện “giảm hơn 30%”.

## Ca sai định dạng và thiếu dữ liệu

| Ca | Thay đổi | Kết quả mong đợi và điểm xác minh |
| --- | --- | --- |
| V01 | Xóa `tuoi` khỏi bản ghi N05. | `THEO_DOI` / `null`. Lý do nêu thiếu tuổi. |
| V02 | Thử từng giá trị tuổi `"25"`, `True`, số âm và `NaN`. | `THEO_DOI` / `null`, với lý do “Đầu vào không hợp lệ”. |
| V03 | Thử cờ hô hấp `"true"` hoặc `1`, và HATT `"120"`, `120.0` hoặc số âm. | Cùng kỳ vọng với V02, kiểm tra riêng từng giá trị. |
| V04 | Thêm một trường ngoài Data Dictionary với giá trị đánh dấu giả lập. | `THEO_DOI` / `null`, với lý do “Đầu vào không hợp lệ”. Giá trị đánh dấu không xuất hiện trong lý do hoặc audit. |
| C01 | Từ N03, bật thêm cờ da để đồng thời khớp R02 và R03. | `PHAN_VE` / `R02-PV`. |
| C02 | Xóa `tuoi` khỏi N01. | `THEO_DOI` / `null`. Lý do nêu thiếu tuổi. |
| C03 | Từ N01, thử HATT `null`, rồi thử xóa khóa HATT. | Cả hai trả `PHAN_VE` / `R01-PV`. Lý do nêu thiếu HATT để đánh giá sốc. |
| C04 | Từ N02, đặt HATT 110 và thử huyết áp nền `null`, vắng mặt hoặc bằng 0. | Cả ba trả `PHAN_VE` / `R02-PV`. Lý do nêu dữ liệu nền chưa đủ để tính mức giảm. |
| C05 | Xóa cờ hô hấp khỏi N01, giữ cờ tuần hoàn bằng `false`. | `THEO_DOI` / `null`. Lý do nêu thiếu dữ liệu để xác định kịch bản. |
| C06 | Từ N02, đặt HATT 89 và xóa khóa HATT nền. | `SOC_PHAN_VE` / `R-SOC`. Điều kiện HATT hiện tại vẫn đánh giá được. |

## Audit, khả năng chạy lại và CI

- Trên một ca hợp lệ và một ca sai định dạng, kiểm tra đúng một bản ghi audit mỗi lần gọi. Tập trường phải khớp A-06. Kiểm tra payload giả lập và giá trị đánh dấu của V04 không bị ghi vào log hoặc lý do trả về.
- Với A-02, review code để phát hiện nhánh xử lý dựa trên tên, ID hoặc giá trị gắn riêng với fixture. Dùng các biến thể ở B07 để kiểm tra cùng một bộ cờ cho kết quả khác nhau đúng theo ngưỡng huyết áp. Kiểm tra `ly_do` có thể giải thích quy tắc đã khớp và không có lời khuyên điều trị.
- Trên bản checkout sạch, chạy `python -m pip install -r requirements.txt` rồi `python -m pytest -q`. Cấu hình CI chạy bộ test khi có Pull Request. Lưu link lần chạy và kết quả thực tế vào báo cáo test ở giai đoạn triển khai.

## Benchmark dự kiến

Đo thời gian cho từng lần gọi `classify()` với cấu hình audit cục bộ dùng khi nghiệm thu. Chuẩn bị dữ liệu trước khi bấm giờ. Chạy warm-up, sau đó đo ít nhất **1.000 lần** với một tập ca hợp lệ cố định có đủ ba kết quả. Báo cáo p50, p95, số lần đo, lệnh chạy, cấu hình máy, phiên bản Python và commit. Điều kiện A-10 là **p95 < 100 ms**. Ghi rõ cấu hình audit và phạm vi phép đo để nhóm khác chạy lại được.
