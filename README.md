# App chỉnh sửa ảnh

Reference: https://www.youtube.com/watch?v=iZUcX4kYrSM

## Giới thiệu
Ý tưởng là làm một ứng dụng đơn giản kiểu photoshop cover lại hầu hết những gì đã học <br>
Chúng ta có 12 chương bỏ chương 1 thì còn 11, mọi người đăng ký phần việc của mình ở bên dưới:<br>
*VD Phí Minh Hiếu: 2, 7, 8* <br><br>
Daniel To:  3, 8<br>
Djanctic Vu:  <br>
Dương Nhật Huy:  <br>
Nguyễn Hữu Thành:  <br>
Lê Thu Trà:  <br><br>
*P/S Tôi sủi :))*

## Hướng dẫn

Required libraries:

- Tkinter (`sudo apt-get install python3-tk`)
- PIL + imagetk (`sudo apt-get install python3-pil python3-pil.imagetk`)
- OpenCV (`sudo apt-get install python3-opencv`)

Run:<br>
`python main.py`

One can freely add libraries into the project. Please, add them into the requirements list above and notify everyone.

File main.py hầu như không có gì, mọi thứ nằm ở Frontend.py<br>

Sau khi chạy app, mọi người có thể thấy có các nút, mỗi nút tương ứng với 1 hàm mà ta cần làm.

### Thống nhất:<br>
Class Front-end có 4 biến để lưu ảnh bao gồm 
* self.original_image: lưu ảnh nguyên thủy, không thay đổi biến này
* self.editing_image: dùng để processing
* self.filter_image: lưu self.editing_image khi người dùng bấm apply (xem hàm apply_actionO)
* self.display_image: dùng để display lên màn hình (xem hàm display_action())

Nói chung, mọi người hãy load filter_image vào editing_image rồi edit chính trên editing_image rồi gọi *self.display_action(self.editing_image)* (xem hai hàm blur_action và grayscale để hiểu rõ). Mấy hàm Sketch, Emboss, Sepia tôi chỉ đặt vào cho có thôi, mọi người cứ tự nhiên thay đổi tên hàm.