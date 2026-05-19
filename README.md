# 23021208_23021306_23021310_CaroAI
# Caro AI - Trí Tuệ Nhân Tạo

**Chương trình chơi cờ Caro (4 quân liên tiếp) giữa Người và Máy**

Ứng dụng bài tập nhóm môn **Trí tuệ Nhân tạo** - Sử dụng thuật toán Minimax và Alpha-Beta Pruning.

---

## Mô tả dự án

- Bàn cờ kích thước **9x9**
- Người chơi sử dụng **X**, Máy sử dụng **O**
- Thắng khi tạo được **4 quân liên tiếp** (ngang, dọc, chéo)
- Máy sử dụng **Minimax** và **Alpha-Beta Pruning** kết hợp nhiều cải tiến
- Có giao diện đồ họa bằng Pygame
---

## Tính năng chính

- Chơi Người vs Máy
- Chọn chế độ AI: **Minimax** hoặc **Alpha-Beta Pruning**
- Hiển thị thông tin nước đi của AI (điểm số, số nút đã xét, thời gian)
- Giao diện đồ họa thân thiện

---

##  Yêu cầu hệ thống

- **Python 3.8+**
- Các thư viện cần thiết (xem `requirements.txt`)

---

##  Cài đặt

1.Clone repository
Link GitHub: (https://github.com/letmefeed99-oss/23021208_23021306_23021310_CaroAI)

2. Cài đặt các thư viện
   pip install -r requirements.txt
   
3. Cách chạy chương trình
   Chạy giao diện chơi game (Chính):
python game_gui.py

   Hoặc chạy trực tiếp trên màn hình console
python main.py

Hướng dẫn chơi

 Chạy python game_gui.py
* Dùng chuột trái click vào ô trống để đặt quân X
* Máy sẽ tự động suy nghĩ và đánh quân O
* Người thắng khi có 4 quân liên tiếp
* Click vào "Choi lai"  để chơi lại ván mới

 Chạy python main.py ( chơi trên màn hình console )
* Chọn thuật toán AI:
  1. Minimax
  2. Alpha-Beta (khuyên dùng)
Nhập 1 hoặc 2
* Chọn độ sâu tìm kiếm (càng cao AI càng mạnh nhưng chậm hơn):
  Gợi ý: 2–3 cho Minimax, 4–6 cho Alpha-Beta
Nhập độ sâu (1-8)
* Chọn hàng và cột ( vd : 4 5  là bạn đánh tại hàng 4 cột 5 )
* Người thắng khi có 4 quân liên tiếp
* 'q' để thoát trò chơi
 
