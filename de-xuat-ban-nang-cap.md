# Đề xuất bản nâng cấp — Làm chủ Vibe Code 3D

Bản FREE giúp người mới đi từ ảnh nhân vật đến game Mira chơi được và một landing page chuyển cảnh. Bản nâng cấp nên mở rộng **từng sản phẩm thật**, mỗi module có file thực hành, prompt, hình trước/sau và một kết quả chạy được. Các tên dưới đây là định hướng nội dung, chưa phải lời hứa tính năng đã hoàn thành.

| Module dự kiến | Thuật ngữ đáng học | Bài thực hành khả thi |
|---|---|---|
| **Blender · Hoàn thiện asset 3D** | Topology, UV, material, skin weight, LOD | Sửa một chi tiết áo/bốt của Mira; xuất GLB và so với bản trước trong game. |
| **Animation · Chuyển động tự nhiên** | Rig, retargeting, animation blending, root motion, foot contact | So dáng đứng/đi/chạy trong Xưởng chuyển động; giảm trượt chân và chuyển động giật. |
| **Game nhiều màn · AI quái** | State machine, spawn, difficulty curve, level design | Thêm một khu vực mới và một loại quái có ba trạng thái: tuần tra, đuổi theo, tấn công. |
| **Database · Đăng nhập · Lưu game** | Auth, database, cloud save, dữ liệu người chơi | Tạo hồ sơ người chơi và lưu màn đã qua. Có chế độ khách trước, tài khoản là bước mở rộng. |
| **PWA · Chơi offline** | Service worker, cache, installable web app | Cài bản web lên màn hình chính và chơi lại màn mẫu khi mất mạng sau lần tải đầu. |
| **Mobile launch · Đưa game lên điện thoại** | Responsive controls, performance budget, packaging | Hoàn thiện nút chạm, kiểm máy thật; phân biệt PWA với bản đóng gói để phát hành qua cửa hàng ứng dụng. |
| **Game giáo dục · Gamification** | Learning objective, quest, feedback, progress | Biến một màn thành bài học có nhiệm vụ, phản hồi đúng/sai và ghi lại tiến độ. |
| **Thương mại hóa · Analytics** | Funnel, event, retention, entitlement | Đo lượt vào/chơi xong màn; thử gói nội dung mở rộng và giải thích cách công bố giá rõ ràng. |
| **Landing page GLB tương tác** | 3D viewer, hotspot, lazy loading, fallback | Cho người xem xoay một model, bấm điểm chú thích; vẫn có ảnh dự phòng trên máy yếu. |

**Thứ tự ưu tiên:** hoàn thiện asset và animation → thêm một màn chơi có mục tiêu → lưu tiến độ → thử offline/mobile → ứng dụng vào giáo dục và thương mại hóa. Landing page GLB có thể học độc lập sau chương 11 của bản FREE.

**Điều kiện mở mỗi module:** có sản phẩm mẫu chạy được, ảnh/video chụp từ kết quả thật, prompt mẫu, file tải về, lỗi thường gặp và checklist kiểm trên desktop/mobile. Menu HTML hiện khóa **Coming soon**; không dẫn đến trang trống hay form mua.
