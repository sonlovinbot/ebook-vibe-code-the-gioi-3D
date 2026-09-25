# Tiến độ ebook — Làm chủ Vibe Code 3D

**Ngày cập nhật:** 25/09/2026  
**Phạm vi hiện tại:** nội dung và dàn ý; chưa dàn trang DOCX/PDF theo yêu cầu tác giả.

| Phần | Trạng thái | Ghi chú |
|---|---|---|
| Đề cương 11 chương | Đã cập nhật | Chương 1–10 theo case Mira; Chương 11 mới chuyển sang landing page motion |
| Chương 1–2 | Đã cập nhật để duyệt | Hai góc Tripo H3.1 mới, ảnh game desktop/mobile và thuật ngữ gắn với Mira |
| Chương 3–5 | Đã mở rộng bằng hình để duyệt | Chương 3 có năm mốc game thật, bản đồ concept, bốn khung truyện và bảng giải thích phản hồi; Chương 4–5 có prompt đánh giá/sửa lỗi |
| Chương 11 — Atlas Hành Tinh | Đã tách thành dự án riêng | Mockup, ba cảnh, quy trình và prompt không dùng ảnh Mira; phân biệt MP4 và GLB tương tác |
| Chương 6–7 | Đã đối chiếu repo mới | Retopo, bộ xương Tripo, GIF idle/walk/jump; file Tripo xuất không có clip, game tạo chuyển động bằng mã trên 65 xương |
| Chương 8–10 | Đã mở rộng để duyệt | Sơ đồ hệ thống từ repo, ảnh nhặt Linh Tinh, Xưởng chuyển động, trùm và mobile; Chương 10 kết thúc case Mira |
| Phụ lục A–B | Bản thảo | Từ điển và bộ prompt/checklist dùng ngay |
| HTML preview | Đã dựng | `ebook-reader.html` từ 11 chương + 2 phụ lục; giao diện PC không có bảng chỉnh kích thước, mục lục có bốn menu nâng cấp bị khóa |
| Dàn trang DOCX/PDF | Chưa bắt đầu | Làm sau khi tác giả duyệt nội dung theo quy trình skill |

**Tài sản đã có:** ảnh preview Tripo H3.1, GIF Tripo, ảnh Xưởng chuyển động và game desktop/mobile từ repo, bộ concept tư thế Mira và quái. Chương landing page dùng bộ ảnh riêng của Atlas Hành Tinh. Ảnh game do tác giả cung cấp là kết quả thật; mockup và concept được ghi rõ là định hướng. Ảnh SpaceEdu chỉ là tham khảo bố cục.

**Model Mira:** GLB đời đầu của game có một mesh và texture, chưa có rig/animation. Repo mới nhất dùng `mira-rigged.glb` có 65 xương; chuyển động được dựng bằng mã trên bộ xương. Tripo đã Retopo và Auto Rig, nhưng các GLB xuất ra không chứa clip hoạt ảnh dùng được. Chương 7 phân biệt rõ GIF preview Tripo với chuyển động thực sự trong game. Vòng biên tập ebook này không dùng thêm credit.

**Hình giải thích:** các chương chuyên sâu có thêm ảnh thật, concept và bảng chú giải ngay cạnh nội dung. Bộ SVG mới nằm trong `ebook-assets/visual-boards/` và tái tạo bằng `build_visual_boards.py`; sơ đồ nền tảng cũ nằm trong `ebook-assets/diagrams/`.
