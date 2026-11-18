# PROGRESS — N37 — Track A

- Starter: `ktpmud-bkt-ruleengine-starter` · tag `bkt-2026-v1`
- Fork: <https://github.com/nhom-37/ktpmud-bkt-ruleengine-starter>

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria

Nhóm đã chuẩn bị yêu cầu, kế hoạch kiểm thử và ADR cho Checkpoint 1. Các mục `Đang` dưới đây ghi rõ phần đã chuẩn bị. [Hồ sơ Checkpoint 1 của N37][cp1]

| Mã | Trạng thái (Chưa / Đang / Xong) | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Chưa | [`classifier.py`](../rule_engine/classifier.py) | Hàm `classify()` còn là khung của starter. |
| A-02 | Chưa | [`REQUIREMENTS.md`](../REQUIREMENTS.md) | Đã ghi tiêu chí triển khai dựa trên dữ liệu đầu vào. Kiểm tra code sau khi hiện thực. |
| A-03 | Chưa | [`TEST_PLAN.md`](../TEST_PLAN.md) | Đã xác định các ca cho ba kết quả và ba kịch bản phản vệ. Chờ triển khai và chạy test nghiệp vụ. |
| A-04 | Đang | [`REQUIREMENTS.md`](../REQUIREMENTS.md) · [`TEST_PLAN.md`](../TEST_PLAN.md) | Đã ghi chính sách cho dữ liệu thiếu, sai kiểu hoặc ngoài miền và kỳ vọng của các ca tương ứng. |
| A-05 | Đang | [`REQUIREMENTS.md`](../REQUIREMENTS.md) | Đã xác định `ly_do` phải truy vết được quy tắc hoặc tình trạng đầu vào. |
| A-06 | Đang | [`DECISIONS.md`](../DECISIONS.md) · [`TEST_PLAN.md`](../TEST_PLAN.md) | Đã xác định bốn trường audit và cách kiểm tra nội dung bản ghi. Cần hiện thực cơ chế ghi và test. |
| A-07 | Đang | [`TEST_PLAN.md`](../TEST_PLAN.md) · [Test khung](../tests/test_classifier.py) | Đã lập kế hoạch cho ca thường, sát ngưỡng, sai kiểu và thiếu dữ liệu. Test trong starter hiện kiểm tra trạng thái hàm khung. |
| A-08 | Chưa | [Đính chính #16 của thầy][ci-erratum] | Cần áp dụng cấu hình `pytest.ini`, sau đó chạy `pytest -q` từ bản checkout sạch và lưu kết quả. |
| A-09 | Đang | [Workflow của starter](../.github/workflows/test.yml) | Workflow đã có trigger Pull Request. Cần chạy test nghiệp vụ trên PR nội bộ trong fork và lưu link lần chạy. |
| A-10 | Đang | [`TEST_PLAN.md`](../TEST_PLAN.md) | Đã lập phương án đo ít nhất 1.000 lượt sau warm-up. Kết quả p50 và p95 sẽ ghi sau khi đo. |
| A-11 | Chưa | [`README.md`](../README.md) | Cần thêm nhãn `educational/synthetic — not for clinical use`. |

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1

| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Không có mục ❗ riêng đã nhận đến thời điểm lập báo cáo | Không có | [Hồ sơ Checkpoint 1 của N37][cp1] |

### 1.3. Timeline dự kiến đến khi hoàn thành

| Việc | Vai trò phụ trách | Mốc (CP2 15/11 · M3 · Freeze 19/11 · M4 20/11) | Ngày dự kiến |
|---|---|---|---|
| Triển khai kiểm tra đầu vào và phân loại theo bảng V1, gồm `rule_id` và `ly_do` | Logic | CP2 | 13/11 |
| Thêm audit, viết test nghiệp vụ và chạy CI trong fork | Logic, Kiểm thử/CI | CP2 | 15/11 |
| Chuẩn bị và chạy thử demo với dữ liệu giả lập | Cả nhóm | CP2 | 15/11 |
| Đo benchmark, ghi báo cáo test, rà soát bảo mật và cập nhật README | Kiểm thử/CI, Tài liệu/Nộp bài | M3 | 17/11 |
| Mở Draft PR nộp bài vào `ktpmud-project` và kiểm tra `validate` | Tài liệu/Nộp bài, Kiểm thử/CI | PC-2, trước 11:30 | 18/11 |
| Chốt code, tài liệu và bằng chứng CI. Gắn tag `bkt-2026-N37-rc1` trước 23:59 | Cả nhóm | Freeze | 19/11 |
| Chuyển Draft PR sang Ready for review | Tài liệu/Nộp bài | M4 | 20/11 |

[Yêu cầu Draft PR cho PC-2][draft-erratum]

### 1.4. Rủi ro / đang vướng

- `classify()` còn ở trạng thái khung. Ưu tiên chạy được luồng phân loại với dữ liệu giả lập, sau đó mở rộng test quanh các ngưỡng tuổi và huyết áp.
- Fork còn cần áp dụng cấu hình pytest theo đính chính #16. Sau khi cấu hình, nhóm sẽ chạy lại test trên máy và trên CI. [Đính chính #16][ci-erratum]

### 1.5. Câu hỏi cho GV

- Q1: Nhờ thầy hoặc trợ giảng xác nhận hồ sơ Checkpoint 1 của N37 đã được ghi nhận khi nhóm đính kèm link ở PC-1. [Hồ sơ Checkpoint 1 của N37][cp1]

### 1.6. Phân công (alias hoặc vai trò, KHÔNG ghi họ tên/MSSV)

| Alias / vai trò | Đầu việc chính | Commit/PR tiêu biểu |
|---|---|---|
| Logic | Triển khai `classify()`, xử lý dữ liệu đầu vào và ghi audit. | [ADR trong hồ sơ CP1][cp1] là cơ sở triển khai. |
| Kiểm thử/CI | Viết test nghiệp vụ, cấu hình pytest, chạy CI và benchmark. | [Kế hoạch test trong hồ sơ CP1][cp1] là cơ sở kiểm thử. |
| Tài liệu/Nộp bài | Cập nhật README, báo cáo, hồ sơ đóng góp và chuẩn bị PR nộp bài. | [Commit tài liệu Checkpoint 1][cp1] |

## PC-2 — 18/11/2026

### 2.1. Đối chiếu timeline PC-1

| Việc | Kế hoạch | Thực tế | Lệch & lý do |
|---|---|---|---|
| Phân loại, audit và test | 15/11 | Hoàn thiện và chạy cục bộ 18/11 | Muộn so với dự kiến. |
| Benchmark và tài liệu | 17/11 | Đã đo và tạo hồ sơ 18/11 | Muộn so với dự kiến. |
| Demo và Draft PR | 15/11 và 18/11 | Đã có kịch bản demo và hồ sơ Draft PR cục bộ | Chờ xác nhận CI và tạo PR. |

### 2.2. Tiến độ theo acceptance criteria

| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| A-01 | Xong | [Classifier](../rule_engine/classifier.py) | Hàm trả kết quả theo hợp đồng V1. |
| A-02 | Xong | [Classifier](../rule_engine/classifier.py) | Đánh giá từ dữ liệu, không dựa trên mã ca. |
| A-03 | Xong | [Bộ test](../tests/test_classifier.py) | Đã chạy ca cho cả ba mức. |
| A-04 | Xong | [Bộ test](../tests/test_classifier.py) | Đã chạy ca thiếu và sai kiểu. |
| A-05 | Xong | [Bộ test](../tests/test_classifier.py) | Kiểm tra mã trong lý do. |
| A-06 | Xong | [Bộ test](../tests/test_classifier.py) | Kiểm tra bốn khóa audit và UUID phiên. |
| A-07 | Xong | [Bộ test](../tests/test_classifier.py) | Có ca thường, ngưỡng, sai kiểu và thiếu dữ liệu. |
| A-08 | Đang | [Báo cáo test](../TEST_REPORT.md) | Unittest đạt. Cần xác nhận pytest trên bản checkout sạch. |
| A-09 | Đang | [Workflow](../.github/workflows/test.yml) | Cần kích hoạt và xác nhận CI trên GitHub. |
| A-10 | Xong | [Báo cáo test](../TEST_REPORT.md) | Đã đo 3.000 lượt sau warm-up. |
| A-11 | Xong | [README](../README.md) | Đã thêm nhãn giáo dục và dữ liệu giả lập. |

### 2.3. Sẵn sàng nộp bài

| Deliverable | Có / Chưa | Đường dẫn |
|---|---|---|
| README, yêu cầu và ADR | Có | [README](../README.md) · [Yêu cầu](../REQUIREMENTS.md) · [ADR](../DECISIONS.md) |
| Test tự động + CI xanh | Chưa | [Bộ test](../tests/test_classifier.py) · [Báo cáo](../TEST_REPORT.md) |
| Báo cáo test và checklist bảo mật | Có | [Test](../TEST_REPORT.md) · [Checklist](../SECURITY_PRIVACY_CHECKLIST.md) |
| AI-use và phân công | Có bản đang làm | [AI](../AI_USE.md) · [Đóng góp](../CONTRIBUTIONS.md) |
| Kịch bản demo | Có | [Demo](../DEMO_SCRIPT.md) |
| Draft PR có check validate xanh | Chưa | [Yêu cầu PC-2][draft-erratum] |

### 2.4. Việc còn lại đến Freeze

| Việc | Vai trò phụ trách | Hạn |
|---|---|---|
| Push code, xác nhận test CI và kiểm tra hồ sơ trên Draft PR | Kiểm thử/CI, Tài liệu/Nộp bài | Trước Freeze |
| Rà soát đóng góp, chạy thử demo và chốt SHA/tag | Cả nhóm | 23:59 19/11 |

### 2.5. Rủi ro / câu hỏi cho GV

- Cần xác nhận CI và `validate` trên GitHub. Báo cáo test hiện ghi kết quả cục bộ.

## Kết quả cuối — Freeze 19/11/2026

- Tag dự kiến: `bkt-2026-N37-rc1`. Ghi SHA tại Freeze.
- Trạng thái cuối từng mã AC: cập nhật bảng 2.2 tại Freeze.
- Những việc trong timeline chưa hoàn thành và lý do: cập nhật tại Freeze.

[cp1]: https://github.com/nhom-37/ktpmud-bkt-ruleengine-starter/tree/7b647ce4a8986d6e4f2f090a23f379cf4f517803
[ci-erratum]: https://github.com/fossbk-spec/ktpmud-project/issues/16
[draft-erratum]: https://github.com/fossbk-spec/ktpmud-project/issues/28
