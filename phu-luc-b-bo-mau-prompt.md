# Phụ lục B — Bộ mẫu thực hành nhanh

Các mẫu này gom những câu lệnh dùng lại nhiều lần. Thay nội dung trong `[ngoặc vuông]`; bỏ câu nào không đúng dự án. Sau mỗi prompt, hãy **mở bản thật và tự thử**, không chỉ đọc câu trả lời của agent.

## B1. Phiếu brief một trang

```text
Tên dự án: [tên]
Người xem: [ai]
Mục tiêu của người xem: [một hành động]
Asset đã có: [tên file + định dạng + tình trạng đã duyệt]
Bắt buộc: [tối đa ba điều]
Để sau: [tối đa ba điều]
Thiết bị cần thử: [desktop/điện thoại]
Đạt khi: [ba việc quan sát hoặc thao tác được]
```

## B2. Tạo dự án nhỏ

> Tôi mới bắt đầu và có brief này: `[dán brief]`. Hãy chọn bản đơn giản nhất có thể chạy trong trình duyệt. Trước khi sửa file, chia thành tối đa năm mốc và nói rõ tôi phải nhìn thấy gì sau mỗi mốc. Chỉ làm mốc đầu sau khi tôi duyệt. Nếu thiếu asset, nêu điều thiếu; đừng dùng ảnh giả rồi nói là đã hoàn thành.

**Thử:** mốc đầu mở được; thông điệp và thao tác chính nhìn thấy. **Lỗi:** gửi ảnh hoặc log theo B4.

## B3. Kiểm GLB trước khi lập trình

> Hãy đọc `[file].glb` và báo: kích thước, mesh/node, vật liệu/texture, skin/rig và clip animation. Với yêu cầu `[xe chạy/bánh quay/nhân vật đi]`, phân biệt phần làm được ngay với phần cần sửa/xuất lại asset. Chưa thay mô hình hoặc viết hiệu ứng cho đến khi báo cáo xong.

**Thử:** báo cáo có tên node/clip hoặc ghi rõ không có. **Lỗi:** nếu kết luận quá chung, yêu cầu bằng chứng từ cấu trúc file.

## B4. Báo một lỗi cụ thể

> Mong muốn: `[điều cần thấy]`. Thực tế: `[điều đã thấy]`. Cách tái hiện: `[các bước]`. Bằng chứng: `[ảnh/log/video]`. Thay đổi gần nhất: `[việc vừa làm]`. Hãy tìm nguyên nhân theo dữ kiện, sửa nhỏ nhất có thể, giữ `[phần đã đúng]`, chạy lại các bước trên và báo kết quả.

**Thử:** lặp đúng các bước tái hiện; kiểm thêm phần đã đúng. **Lỗi:** nếu ba lần chưa tiến bộ, dừng sửa và xem lại giả định/asset.

## B5. Hero video một cảnh

> Xây hero cho `[chủ đề]` với `hero.mp4` làm video nền im lặng và `poster.jpg` làm ảnh chờ. Tiêu đề `[text]`, mô tả `[text]`, CTA `[nhãn + đích thật]` là HTML. Giữ chữ đọc được suốt video, điện thoại không cắt mất chủ thể, người chọn giảm chuyển động xem poster tĩnh. Chỉ làm hero trước; mở preview và thử video, poster, CTA, desktop và màn hẹp.

**Thử:** tải lại, tắt video, bấm CTA, thử màn hẹp. **Lỗi:** ghi giây cụ thể khiến chữ chìm hoặc vùng bị cắt.

## B6. Kiểm trước khi chia sẻ

> Hãy kiểm bản dự án hiện tại trên desktop và điện thoại: nội dung, asset tải được, thao tác chính, CTA, tốc độ cảm nhận, fallback và thông tin nhạy cảm. Lập bảng đã đạt/chưa đạt/chưa thể kiểm. Chỉ sửa lỗi chặn người dùng hoàn thành hành động chính. Sau đó cho tôi biết link nào người khác có thể mở được; đừng gọi localhost là link công khai.

**Thử:** mở link từ thiết bị/trình duyệt khác. **Lỗi:** nếu file lỗi chỉ ở bản chia sẻ, kiểm đường dẫn asset và cấu hình phát hành.

## B7. Checklist bốn ảnh cho Tripo

- [ ] Cùng một đối tượng, cùng màu và phụ kiện ở trước/sau/trái/phải.
- [ ] Mỗi ảnh một góc rõ, toàn thân/toàn xe, nền sạch.
- [ ] Không có chữ, tay/chân/bánh bị cắt hoặc chi tiết che khuất lớn.
- [ ] Đặt bốn ảnh cạnh nhau và đánh dấu chi tiết không nhất quán.
- [ ] Duyệt preview nhiều góc trước khi xuất GLB; kiểm rig/clip riêng.

## B8. Nâng Mira từ di chuyển cả khối sang chạy có khớp

> Đây là repo Mira và GLB mới sau khi Auto Rig. Hãy liệt kê skeleton, skin và tên các clip có thật. Giữ bản GLB cũ làm dự phòng. Nối clip đứng khi không di chuyển, clip chạy khi di chuyển và clip đánh khi dùng chiêu chém. Kiểm khi bắt đầu chạy, đổi hướng và dừng: chân không trượt, bốt không xuyên nền, áo và túi không kéo méo. Mở localhost, cho tôi xem ba trạng thái ở cùng góc camera. Chưa sửa quái và bối cảnh.

**Thử:** đứng → chạy → dừng → chém. **Lỗi:** nếu không có clip, dừng và xử lý asset; đừng gọi chuyển động cả khối là chạy có khớp.

## B9. Nâng một loại quái

> Trong game Mira, hãy xem ảnh concept quái tôi gửi và chọn **một** loại quái hiện tại để nâng cấp hình ảnh. Giữ nguyên máu, tốc độ, thời điểm xuất hiện và kiểu tấn công. Đề xuất giữ hình khối Three.js hay tạo GLB riêng, giải thích lựa chọn bằng việc quái có đọc rõ ở góc camera đang chơi không. Làm một bản thử và mở localhost để tôi so trước/sau.

**Thử:** nhận ra quái khi nó còn ở xa và khi nhiều con cùng xuất hiện. **Lỗi:** nếu model đẹp nhưng khó thấy, chỉnh hình/màu trước khi tăng chi tiết.

## B10. Đồng bộ một chiêu phép

> Hãy kiểm riêng chiêu Tia Linh Quang của Mira theo ba lớp: luật trúng đích, tư thế nhân vật và hiệu ứng hình/âm. Giữ nguyên sát thương và thời gian hồi. Khi bấm, tư thế và tia sáng phải xuất hiện đúng lúc; quái mất máu khi tia chạm. Hiệu ứng không được che vòng cảnh báo nguy hiểm. Thử với quái đứng gần và quái đang di chuyển; báo điều đã kiểm.

**Thử:** quan sát lúc bấm, tia chạm, thanh máu quái và lúc chiêu sẵn sàng lại. **Lỗi:** nếu ảnh và luật lệch thời điểm, sửa đồng bộ trước khi thêm hạt hoặc ánh sáng.
