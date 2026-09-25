# Phụ lục A — Từ điển đủ dùng cho Vibe Code 3D

Tra từ khi cần; bạn không phải học thuộc trước khi bắt đầu. Ví dụ dưới đây gắn với các bài trong sách.

| Thuật ngữ | Hiểu bằng tiếng thường | Khi bạn cần nhắc đến |
|---|---|---|
| Vibe coding | Diễn đạt mục tiêu, điều kiện và phản hồi bằng ngôn ngữ tự nhiên để agent viết/sửa mã | Giao một mốc dự án cho Codex hoặc Claude |
| Agent lập trình | Trợ lý làm việc với file, có thể chạy và kiểm dự án trong phạm vi quyền được cấp | Muốn tạo trang thật thay vì chỉ xin ý tưởng |
| GPT-6 Astra / Claude Fable 5.1 | Tên model tác giả chọn cho ví dụ; khả năng và nhãn có thể đổi | Chọn model đang được tài khoản hỗ trợ; không xem tên model là bảo đảm chất lượng |
| Codex | Agent lập trình trong hệ sinh thái OpenAI | Nhờ đọc repo, tạo/sửa web 3D, kiểm file |
| Token | Đơn vị AI xử lý khi đọc và sinh nội dung | Cần giữ ngữ cảnh gọn, đưa log/ảnh liên quan |
| Brief | Tờ giao việc nêu mục tiêu, người xem, asset, giới hạn và cách kiểm | Trước khi viết prompt dự án |
| Asset | File dùng trong dự án: ảnh, video, model, âm thanh | Kiểm đầu vào và quyền sử dụng |
| Scene | Không gian chứa các đối tượng 3D | Khi model đã tải nhưng chưa thấy trong cảnh |
| Camera | Góc mắt người xem nhìn vào cảnh | Khi đối tượng bị cắt hoặc quá nhỏ |
| Mesh / geometry | Hình khối 3D và cấu trúc hình dạng | Khi giày, bánh xe hoặc khuôn mặt bị méo |
| Material / texture | Tính chất bề mặt và ảnh vẽ chi tiết lên bề mặt | Khi màu áo hoặc sơn xe không đúng |
| Light | Nguồn sáng trong cảnh | Khi model tối dù file đã tải |
| HDR / environment map | Hình môi trường giúp tạo ánh sáng/phản chiếu xung quanh | Khi vật liệu kim loại trông phẳng hoặc đen |
| Renderer | Bộ phận biến scene và camera thành hình trong trình duyệt | Khi trang có mã nhưng không hiện cảnh |
| Three.js | Thư viện giúp dựng và hiển thị 3D trên web | Khi cần GLB tương tác trong trình duyệt |
| WebGL | Nền tảng đồ họa trình duyệt mà thư viện 3D có thể dùng | Không phải app riêng cần cài cho người mới |
| glTF / GLB | Định dạng gói/trao đổi mô hình 3D; GLB thường là một file | Tải model từ Tripo để đưa vào web |
| Node | Một thành phần có tên/vị trí trong cấu trúc model | Kiểm bánh xe có tách riêng hay không |
| Rig / skeleton | Bộ xương gồm các khớp để xoay tay, chân, thân | Khi muốn Mira gập gối hoặc vung tay |
| Skin weight | Mức độ một vùng bề mặt đi theo từng xương | Khi đầu gối gập mà quần, áo hoặc bốt bị méo |
| Pose | Một tư thế của các khớp tại một thời điểm | Khi kiểm một khoảnh khắc đứng, bước hoặc đánh |
| Animation / clip | Chuỗi pose theo thời gian thành một động tác | Khi muốn phát idle, walk hoặc run từ GLB |
| In-place | Clip bước/chạy tại chỗ, không tự kéo nhân vật đi xa | Khi game đã điều khiển vị trí nhân vật |
| Root motion | Chuyển động toàn thân được ghi ngay trong clip | Khi nhân vật tự trôi dù người chơi đã dừng |
| AnimationMixer | Công cụ trong Three.js phát và chuyển giữa các clip | Khi agent nối clip đứng, đi, chạy vào game |
| Shader | Công thức tính màu/bề mặt khi vẽ | Chỉ cần biết khác texture và ánh sáng ở mức nhập môn |
| FPS | Số khung hình hiển thị mỗi giây | Khi xoay hoặc di chuyển bị giật |
| Repo | Kho file dự án, thường có lịch sử thay đổi | Dùng một mẫu có sẵn và phát triển tiếp |
| Skill | Quy trình/hướng dẫn tái sử dụng cho agent | Brainstorm hoặc kiểm chất lượng theo bước |
| Plugin | Gói khả năng/công cụ bổ sung | Khi cần chức năng chuyên biệt |
| MCP | Cách kết nối agent với công cụ/dữ liệu ngoài | Khi muốn agent gọi Tripo hoặc dịch vụ khác trong phạm vi được phép |
| Poster | Ảnh tĩnh hiển thị khi video chưa phát/không phát | Hero motion phải vẫn đọc và bấm được |
| Fallback | Phương án dự phòng khi thành phần chính không chạy | Dùng poster nếu MP4 không phát |
| Reduced motion | Tùy chọn giảm chuyển động của người dùng | Chọn ảnh tĩnh hoặc ít chuyển động hơn |
| Console | Nơi trình duyệt báo lỗi kỹ thuật | Gửi dòng lỗi liên quan cho agent |
| Preview / localhost | Bản xem thử, thường chỉ chạy trên máy đang làm | Kiểm trước khi chia sẻ công khai |
| Deploy / phát hành | Đưa dự án lên nơi người khác mở bằng link | Kiểm đường dẫn asset và chức năng từ máy khác |

**Ngoài phạm vi bản nhập môn:** glTFast/Unity WebGL, nền tảng Toy, đo thời gian operator và thao tác Blender chuyên sâu. Chúng liên quan đến quy trình khác, chưa cần để hoàn thành một trang Three.js hoặc landing page motion. Nếu file tác giả gọi là “GLX”, hãy kiểm tên/định dạng thực tế; ví dụ trong sách dùng **GLB/glTF**.
