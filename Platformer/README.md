# Game Platformer 2D -- Python & Pygame

## Giới thiệu

Dự án xây dựng một trò chơi platformer 2D bằng Python và thư viện
Pygame. Người chơi điều khiển nhân vật chính di chuyển trái/phải, nhảy,
vượt qua chướng ngại vật, thu thập item, tránh hoặc tiêu diệt kẻ địch và
hoàn thành từng bản đồ (level).

Hệ thống bao gồm: - Nhân vật chính với hoạt ảnh (animation). - Tile map
để tạo môi trường. - Kẻ địch có hành vi đơn giản. - Vật phẩm cần thu
thập. - Menu chính, màn hình game over, hệ thống điểm số. - Hiệu ứng âm
thanh và hình ảnh. - Lưu/đọc dữ liệu tiến trình bằng pickle.

Dự án củng cố kiến thức Python: xử lý sự kiện, class, module, file
system, collision detection, vật lý đơn giản (gravity, jump), camera
scrolling...

# 1. Mục tiêu của dự án

## 1.1. Mục tiêu kỹ thuật

-   Vận dụng Python vào phát triển ứng dụng thực tế.
-   Sử dụng Pygame để xây dựng loop game, render, update frame, xử lý
    input.
-   Lưu trữ tiến trình bằng pickle.
-   Tải lại game với chức năng load.

## 1.2. Mục tiêu ứng dụng

-   Lưu, quản lý và tải dữ liệu người chơi.
-   Ghi nhận điểm số, số level hoàn thành, thời gian chơi.
-   Tự động hóa nhập/xuất dữ liệu qua file .pkl.

# 2. Cơ sở lý thuyết

## 2.1. Kiến thức Python nền tảng

-   List, Tuple, Dictionary, Set.
-   Thư viện chuẩn: os, datetime, random, json, math.
-   try--except và xử lý lỗi.
-   Đọc/ghi file.
-   Hàm, lambda, \*args, \*\*kwargs.

## 2.2. Phát triển ứng dụng Python

Các dạng ứng dụng: - Console (CLI) - GUI - Web - Ứng dụng có database

Trong dự án này: game real--time bằng Pygame + quản lý dữ liệu bằng
pickle.

# 3. Phân tích & thiết kế ứng dụng

## 3.1. Loại ứng dụng

Game Platformer 2D chạy desktop.

### Tên ứng dụng

2D Platformer Game -- Python & Pygame

### Mục tiêu

-   Xây dựng game 2D hoàn chỉnh.
-   Áp dụng animation, collision, camera.
-   Lưu -- tải tiến trình.

### Phạm vi

-   Chạy trên PC.
-   Không mobile/web.
-   Lưu local.
-   Level đơn giản.

# 3.2. Yêu cầu người dùng

Ứng dụng có 2 nhóm: Admin và Player.

## 3.2.1. Yêu cầu chức năng

### Admin

-   Thêm/sửa/xóa map.
-   Điều chỉnh độ khó.
-   Quản lý dữ liệu người chơi.

### Player

-   Chơi game.
-   Thu thập item, vượt chướng ngại vật.
-   Lưu tiến trình.
-   Tải tiến trình.

## 3.2.2. Yêu cầu phi chức năng

### Hiệu suất

-   RAM 4--8GB.
-   40--60 FPS.

### Bảo mật

-   Không lưu plaintext password.
-   Tránh pickle injection.

### Khả năng mở rộng

-   Dễ thêm map, enemy, item.
-   Code tách module rõ ràng.

# 4. Kết luận

Dự án giúp nắm vững Python và lập trình game qua Pygame. Có thể dùng làm
project cuối kỳ hoặc tiếp tục mở rộng thành game hoàn chỉnh.
