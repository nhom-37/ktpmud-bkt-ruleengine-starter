# Checklist bảo mật và dữ liệu · N37

- Test và benchmark dùng ca giả lập theo Data Dictionary V1.
- Dữ liệu có khóa ngoài Data Dictionary bị từ chối. Lý do trả về dùng mã quy tắc, thông báo cố định và thông tin về trường thiếu.
- Audit chỉ ghi `Timestamp`, `User_UUID`, `Action_Type` và `Status`. UUID đại diện phiên giả lập. Test kiểm tra chính xác tập khóa và tính ổn định của UUID giữa các lần gọi.
- README ghi phạm vi sử dụng cho giáo dục và dữ liệu giả lập.
