# Yêu cầu Checkpoint 1 — Track A · Dr May Day

**Nhóm** N37 · **Mốc** Checkpoint 1, 08/11/2026  
**Starter** `ktpmud-bkt-ruleengine-starter` @ `bkt-2026-v1`

## Mục tiêu và phạm vi

Triển khai `classify(patient)` trong `rule_engine/classifier.py` cho bài tập mô phỏng. Phạm vi gồm đọc và kiểm tra đầu vào, phân loại theo bảng quyết định V1, giải thích kết quả, ghi audit tối thiểu, kiểm thử tự động, CI và benchmark. Dữ liệu dùng trong code, test và demo đều là dữ liệu giả lập.

Ứng dụng bệnh viện, tích hợp production, dữ liệu bệnh nhân thật, chẩn đoán, khuyến nghị điều trị và các quy tắc lâm sàng bổ sung nằm ngoài phạm vi.

## Hợp đồng của hàm phân loại

- **Đầu vào.** Dùng các trường trong Data Dictionary V1. Tuổi tính theo năm và có thể là số lẻ. Huyết áp tâm thu hiện tại và huyết áp nền có kiểu số nguyên hoặc `null`. Các cờ về dị nguyên và triệu chứng có kiểu Boolean. Giữ kiểu `PatientInput` và chữ ký có sẵn trong starter.
- **Phân loại.** Trả `SOC_PHAN_VE` khi ca khớp ít nhất một kịch bản phản vệ và đạt điều kiện huyết áp theo tuổi trong bảng. Khi một kịch bản phản vệ đã được xác định và dữ liệu hiện có chưa đủ điều kiện sốc, trả `PHAN_VE`. Khi chưa xác định được kịch bản nào hoặc thiếu tuổi, trả `THEO_DOI`. Áp dụng kiểm tra dữ liệu trước khi xét các quy tắc.
- **Đầu ra.** Trả `muc_do`, `rule_id` và `ly_do`. Mã quy tắc là `R-SOC`, `R01-PV`, `R02-PV`, `R03-PV` hoặc `null` theo đặc tả. Lý do ngắn, đủ để lần về quy tắc hoặc tình trạng đầu vào. Lý do không chứa dữ liệu lâm sàng thô hoặc lời khuyên điều trị.
- **Audit.** Mỗi lần phân loại ghi đúng bốn trường `Timestamp`, `User_UUID`, `Action_Type` và `Status`. UUID dùng trong môi trường bài thi là định danh giả lập của tác nhân thao tác, tách khỏi hồ sơ đầu vào. Log không chứa triệu chứng, điểm sức khỏe, huyết áp, dữ liệu nhận dạng hoặc bản sao payload.

Nguồn đối chiếu cho các quy tắc và trường dữ liệu. [Bảng quyết định V1](https://raw.githubusercontent.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/bkt-2026-v1/docs/decision-table.md) · [Chữ ký trong starter](https://raw.githubusercontent.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/bkt-2026-v1/rule_engine/classifier.py)

## Tiêu chí nghiệm thu

| ID | Điều kiện đạt | Cách kiểm tra dự kiến |
| --- | --- | --- |
| A-01 | `classify()` chạy theo hợp đồng và trả đủ ba trường. | Gọi hàm trực tiếp trên các ca hợp lệ. |
| A-02 | Kết quả được suy ra từ các trường dữ liệu, độc lập với tên hoặc ID của fixture. | Review code và thử các biến thể đầu vào quanh cùng một ngưỡng để kiểm tra kết quả đổi theo quy tắc. |
| A-03 | Bao phủ ba kết quả và cả ba kịch bản phản vệ trong bảng V1. | Các nhóm ca N và B trong [kế hoạch test](TEST_PLAN.md). |
| A-04 | Đầu vào thiếu, sai kiểu hoặc ngoài miền được xử lý nhất quán theo chính sách công bố. | Đối chiếu kết quả thực tế với kỳ vọng của các nhóm ca V và C. |
| A-05 | `ly_do` truy vết được quy tắc đã khớp và tránh lời khuyên điều trị. | Kiểm tra nội dung kết quả, đồng thời review câu giải thích. |
| A-06 | Mỗi lần phân loại tạo audit với đúng bốn trường và không ghi đầu vào lâm sàng thô. | Kiểm tra bản ghi audit trên cả ca hợp lệ và ca sai định dạng. |
| A-07 | Có unit test cho ca thường, sát ngưỡng, sai đầu vào và thiếu dữ liệu. | Review bộ `pytest` đối chiếu với kế hoạch test. |
| A-08 | `pytest -q` đạt từ bản checkout sạch sau khi cài phụ thuộc theo README. | Chạy lại trên môi trường sạch và lưu kết quả thực tế. |
| A-09 | CI tự động chạy bộ test khi có Pull Request. | Mở PR thử trong fork của nhóm và kiểm tra kết quả workflow. |
| A-10 | Benchmark ít nhất 1.000 lượt sau warm-up, báo cáo p50/p95 và đạt p95 dưới 100 ms trên máy đã khai báo. | Ghi cấu hình máy, Python, commit, lệnh chạy và kết quả đo thực tế. |
| A-11 | README có nhãn `educational/synthetic — not for clinical use`. | Review README ở commit dùng để nghiệm thu. |

Nguồn đối chiếu tiêu chí. [Mục 7.3 của đề](https://fossbk-spec.github.io/ktpmud-book/exams/KTPMUD_Hack_Marathon_2026_De_Thi_Chinh_Thuc_v1.0.0_20261103.html#_7-3-acceptance-criteria-bat-buoc)

## Cách nhóm N37 áp dụng bảng V1

Các ngưỡng và điều kiện phân loại lấy từ bảng V1. Nhóm quy định cách xử lý dữ liệu thiếu hoặc sai định dạng và cách chọn mã giải thích khi nhiều kịch bản cùng khớp.

- **Dữ liệu sai định dạng.** Tuổi nhận số hữu hạn từ 0 trở lên, gồm số nguyên và số lẻ, loại trừ Boolean. Cờ nhận giá trị Boolean. Huyết áp nhận số nguyên không âm hoặc `null`, loại trừ Boolean. Với bản ghi sai kiểu, ngoài miền nêu trên hoặc có trường ngoài Data Dictionary, trả `THEO_DOI`, `rule_id = null` và `ly_do` là “Đầu vào không hợp lệ”. Chuỗi số được xử lý như dữ liệu sai kiểu.
- **Thiếu tuổi.** Khi thiếu trường `tuoi`, trả `THEO_DOI` và `rule_id = null`, kể cả khi các cờ đủ khớp một kịch bản phản vệ. Lý do nêu thiếu tuổi.
- **Nhiều kịch bản cùng khớp.** Khi R02 và R03 cùng khớp và ca cho kết quả `PHAN_VE`, chọn `R02-PV` theo thứ tự trong bảng V1. Nếu ca đạt điều kiện sốc, mã trả về là `R-SOC`.
- **Thiếu huyết áp.** Khóa vắng mặt và `null` đều được xem là thiếu giá trị. Với tuổi hợp lệ và kịch bản phản vệ đã xác định, giữ `PHAN_VE` nếu dữ liệu còn lại chưa xác lập được sốc. Chỉ tính mức giảm phần trăm khi có HATT hiện tại và HATT nền có giá trị lớn hơn 0. Điều kiện theo HATT hiện tại vẫn được xét độc lập khi có giá trị. Khi thiếu dữ liệu để đánh giá sốc, lý do nêu giới hạn đó và dẫn về quy tắc phản vệ đã khớp.
- **Thiếu cờ.** Chỉ xác nhận kịch bản khi các giá trị có mặt đủ chứng minh điều kiện của kịch bản đó. Khi thiếu cờ cần thiết và chưa xác định được kịch bản nào, trả `THEO_DOI` và `rule_id = null`. Cờ vắng mặt được xem là chưa biết.

## Hồ sơ Checkpoint 1

- Yêu cầu và tiêu chí nghiệm thu trong tài liệu này.
- [Kế hoạch kiểm thử](TEST_PLAN.md).
- [ADR đầu tiên](DECISIONS.md).
