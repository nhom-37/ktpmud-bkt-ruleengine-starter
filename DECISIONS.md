# ADR-001 — Tách kiểm tra đầu vào khỏi áp dụng bảng quyết định

**Nhóm** N37 · **Ngày chốt** 08/11/2026  
**Phạm vi** Track A, Checkpoint 1 · **Liên quan** A-01, A-03, A-04, A-05, A-06, A-07

## Bối cảnh

Starter cung cấp `classify(patient)` và kiểu kết quả có sẵn. Bảng quyết định V1 phân biệt phản vệ với sốc phản vệ dựa trên hai tầng điều kiện. Một số dữ liệu có thể thiếu hoặc sai kiểu. Nhóm cần kiểm thử được các ngưỡng và truy vết được kết quả, đồng thời giới hạn dữ liệu ghi trong audit. [Starter](https://raw.githubusercontent.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/bkt-2026-v1/rule_engine/classifier.py) · [Bảng quyết định V1](https://raw.githubusercontent.com/fossbk-spec/ktpmud-bkt-ruleengine-starter/bkt-2026-v1/docs/decision-table.md)

## Quyết định

Giữ `classify(patient)` làm điểm vào duy nhất. Tách kiểm tra kiểu và tình trạng dữ liệu khỏi phần áp dụng bảng quyết định. Khi bản ghi sai định dạng, hàm trả `THEO_DOI`, `rule_id = null` và lý do “Đầu vào không hợp lệ”. Cách này giữ cấu trúc kết quả của starter và cho biết vì sao dữ liệu chưa thể dùng để phân loại.

Phần đánh giá xác định kịch bản phản vệ đã khớp, rồi xét điều kiện huyết áp để chọn kết quả cuối. Nếu đủ điều kiện sốc, trả `R-SOC`. Nhóm áp dụng cách chọn mã và xử lý dữ liệu thiếu đã ghi trong [REQUIREMENTS.md](REQUIREMENTS.md).

Chuẩn bị kết quả và audit tại điểm vào để mỗi lần gọi ghi đúng một bản ghi. Phần tạo audit nhận siêu dữ liệu thao tác và trạng thái, tránh truyền bản ghi lâm sàng sang phần này. Giữ logic phân loại độc lập với việc ghi log để kiểm thử được các nhánh quy tắc.

## Lý do và đánh đổi

Một hàm xử lý chung có thể thuận tiện khi mới viết vài ca. Khi thêm kiểm tra kiểu, ngưỡng tuổi, nhiều quy tắc khớp và audit, việc tách trách nhiệm giúp xem riêng điều kiện nào tạo ra kết quả. Đổi lại, nhóm cần giữ ranh giới rõ và tránh tạo thêm lớp hay cấu hình khi vài hàm nội bộ đã đủ.

## Cách xác minh

Phần triển khai 18/11 dùng một bảng Python gồm mã và hàm điều kiện cho R01, R02, R03. Duyệt theo thứ tự do giảng viên quy định. Bảng giúp tách từng điều kiện khi đọc và kiểm thử. Nếu dùng YAML, nhóm phải bổ sung cơ chế đọc và xác thực cấu hình. [Làm rõ của giảng viên](https://github.com/fossbk-spec/ktpmud-project/issues/15)

Cờ vắng mặt hoặc `null` được xem là chưa biết. Nếu dữ liệu còn lại đủ khớp một quy tắc, sử dụng kết quả đó. Nếu chưa có quy tắc nào khớp, trả `THEO_DOI`. Mỗi tiến trình dùng một UUID giả lập, giữ ổn định giữa các lần gọi. Audit được ghi dưới dạng JSON từng dòng ra stderr.

Dùng các ca N và B để kiểm tra quy tắc cùng ngưỡng, các ca V và C để kiểm tra chính sách đầu vào và mã giải thích. Kiểm tra mỗi lần gọi tạo đúng một bản ghi audit với UUID giả lập và đúng bốn trường đã quy định. [Kế hoạch kiểm thử](TEST_PLAN.md)
