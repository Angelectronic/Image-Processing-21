# App chỉnh sửa ảnh

Reference: https://www.youtube.com/watch?v=iZUcX4kYrSM

## Giới thiệu
Ý tưởng là làm một ứng dụng đơn giản kiểu photoshop cover lại hầu hết những gì đã học <br>
Chúng ta có 12 chương bỏ chương 1 thì còn 11, mọi người đăng ký phần việc của mình ở bên dưới:<br>
*VD Phí Minh Hiếu: 2, 7, 8* <br><br>
Daniel To:  <br>
Djanctic Vu:  <br>
Dương Nhật Huy:  <br>
Nguyễn Hữu Thành:  <br>
Lê Thu Trà:  <br><br>
*P/S Tôi sủi :))*

## Hướng dẫn
Cmd:<br>
`python main.py`

App sử dụng cv2 và tkinter (Có thể thoải mái dùng thêm thư viện, miễn là thông báo cho mọi người để cùng tải)<br>

File main.py hầu như không có gì, mọi thứ nằm ở Frontend.py<br>

Sau khi chạy app, mọi người có thể thấy có các nút, mỗi nút tương ứng với 1 hàm mà ta cần làm.

### Thống nhất:<br>
Class Front-end có 4 biến để lưu ảnh bao gồm 
* self.original_image: lưu ảnh nguyên thủy, không thay đổi biến này
* self.editing_image: dùng để processing
* self.filter_image: lưu self.editing_image khi người dùng bấm apply (xem hàm apply_actionO)
* self.display_image: dùng để display lên màn hình (xem hàm display_action())

Nói chung, mọi người hãy load filter_image vào editing_image rồi edit chính trên editing_image rồi gọi *self.display_action(self.editing_image)* (xem hai hàm blur_action và grayscale để hiểu rõ)