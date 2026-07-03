# Lời thoại Thuyết trình Đồ án Môn học Nhận dạng
**Đề tài:** Chương 20: Face Synthesis (Handbook of Face Recognition 2nd Edition) & Nghiên cứu tiên tiến SynFER  
**Nhóm thực hiện:** Đàm Tiến Đạt, Nguyễn Đăng Khoa, Huỳnh Mạnh Tường  
**Tổng thời lượng thuyết trình:** 30 phút (Khoa: 8 phút | Tường: 8 phút | Đạt: 9 phút lời thoại + 3 phút demo video)

---

## PHẦN MỞ ĐẦU: GIỚI THIỆU TỔNG QUAN
**Người trình bày:** Đàm Tiến Đạt  
**Thời lượng dự kiến:** 30s

### [Slide 1 - Trang bìa]
**Đạt:**  
Em xin chào thầy và các bạn, nhóm chúng em là nhóm 11, gồm ba thành viên: em là Đàm Tiến Đạt, cùng hai bạn Nguyễn Đăng Khoa và Huỳnh Mạnh Tường. Hôm nay, nhóm chúng em xin được trình bày đồ án môn học Nhận dạng với chủ đề **Face Synthesis** được xây dựng dựa trên sự kết hợp giữa lý thuyết nền tảng từ Chương 20 - Face Synthesis của giáo trình *Handbook of Face Recognition* và bài báo SOTA *SynFER: Towards Boosting Facial Expression Recognition with Synthetic Data*.

### [Slide 2 - Mục lục]
**Đạt:**  
Bài thuyết trình của nhóm chúng em được chia thành bốn phần nội dung chính:
- Thứ nhất là **Mô hình hóa khuôn mặt**, nơi chúng ta khám phá cách tái dựng mô hình hình học hình học 3D từ các nguồn dữ liệu ảnh 2D khác nhau.
- Thứ hai là **Chiếu sáng lại khuôn mặt**, nghiên cứu các phương pháp thao túng ánh sáng để chuẩn hóa hoặc tăng cường dữ liệu khuôn mặt.
- Thứ ba là **Tổng hợp biểu cảm khuôn mặt và SOTA paper SynFER**, phần này bao gồm các phân tích đối chiếu giữa lý thuyết trong sách với phương pháp của paper, đồng thời báo cáo kết quả thực nghiệm và mở rộng của nhóm trên các bộ dữ liệu mới.
- Cuối cùng là phần **Demo thực nghiệm hệ thống** nhằm minh họa trực quan năng lực tổng hợp biểu cảm và hỗ trợ bài toán nhận dạng của mô hình.

Sau đây, để mở đầu cho nội dung chi tiết, em xin trân trọng mời bạn Nguyễn Đăng Khoa bắt đầu với phần trình bày về Mô hình hóa khuôn mặt.

---

## PHẦN 1: MÔ HÌNH HÓA KHUÔN MẶT
**Người trình bày:** Nguyễn Đăng Khoa  
**Thời lượng dự kiến:** 8 phút

### [Slide 4 - Mô hình hóa khuôn mặt: Tổng quan]
**Khoa:**  
Xin cảm ơn Đạt. Mình là Nguyễn Đăng Khoa, và sau đây mình xin trình bày về nội dung đầu tiên: **Mô hình hóa khuôn mặt**.  
Trong lĩnh vực nhận dạng và thị giác máy tính, mô hình hóa khuôn mặt đóng vai trò đặt nền móng kiến trúc cho toàn bộ các hướng tổng hợp sau này. Mục tiêu cốt lõi của bài toán là tái dựng cấu trúc hình học 3D của một khuôn mặt cá nhân từ thông tin hình ảnh 2D thu thập được. Giáo trình đã phân chia bài toán này theo ba hướng tiếp cận phụ thuộc vào nguồn dữ liệu đầu vào: tái dựng từ chuỗi ảnh video, từ hai ảnh trực giao và từ một ảnh đơn duy nhất. Các mô hình 3D sau khi được tái dựng chính xác không chỉ phục vụ hệ thống nhận dạng khuôn mặt đa góc độ mà còn được ứng dụng rộng rãi trong công nghiệp điện ảnh, trò chơi điện tử và xây dựng các đại diện tương tác thực tế ảo.

### [Slide 5 - Tái dựng từ chuỗi ảnh]
**Khoa:**  
Trước hết, với hướng tiếp cận từ chuỗi ảnh hoặc video, thách thức lớn nhất là làm sao duy trì tính nhất quán hình học khi khuôn mặt biến dạng qua các khung hình. Nghiên cứu tiêu biểu của Liu và các cộng sự năm 2001 đã đề xuất xây dựng một không gian tuyến tính hình học khuôn mặt được biểu diễn bằng phương trình tổ hợp: một khuôn mặt bất kỳ được xác định bằng khuôn mặt trung lập cộng với tổng có trọng số của các metric biến dạng tuyến tính. Các hệ số biến dạng này được giới hạn trong một khoảng giá trị hợp lệ, đảm bảo rằng mọi mô hình được sinh ra trong không gian này đều giữ được cấu trúc tự nhiên của khuôn mặt con người mà không bị biến dạng bất thường. Điểm vượt trội của phương pháp này là sau khi người dùng khởi tạo thủ công bằng cách chọn 5 điểm đặc trưng cơ bản, hệ thống sẽ tự động theo dõi và khớp mô hình cho toàn bộ chuỗi ảnh tiếp theo.

### [Slide 6 - Bài toán khớp mô hình: Giải lặp ICP]
**Khoa:**  
Để tối ưu hóa độ khớp giữa mô hình 3D tham số hóa và tập các điểm đặc trưng phát hiện trên ảnh 2D, các tác giả đã chuyển hóa về bài toán cực tiểu hóa tổng khoảng cách chiếu. Do hệ phương trình chứa cả các biến chuyển động phi tuyến bao gồm ma trận xoay, vectơ tịnh tiến và tỉ lệ biến dạng, cùng với các hệ số hình học tuyến tính, việc giải trực tiếp là vô cùng khó khăn. Vì vậy, thuật toán lặp điểm gần nhất được áp dụng theo hai bước xen kẽ. Ở bước thứ nhất, hệ số hình học được cố định để giải bài toán ước lượng chuyển động bằng phương pháp quaternion nhằm tìm tư thế camera tối ưu. Ở bước thứ hai, tư thế camera được giữ nguyên để giải hệ phương trình tuyến tính cho các hệ số hình học. Quá trình lặp qua lại này hội tụ rất nhanh, giúp mô hình bám sát vào khuôn mặt thực tế trong chuỗi video một cách chính xác.

### [Slide 7 - Điều chỉnh bó dựa trên mô hình]
**Khoa:**  
Một bước tiến quan trọng khác trong việc tái dựng từ chuỗi ảnh là kỹ thuật điều chỉnh bó dựa trên mô hình do Shan và các cộng sự giới thiệu năm 2001. Trong kỹ thuật điều chỉnh bó truyền thống của thị giác máy tính, các tọa độ điểm 3D trong không gian được coi là các biến tự do hoàn toàn, dẫn đến không gian tối ưu hóa cực kỳ lớn và dễ bị nhiễu do sai số trích xuất điểm ảnh. Phương pháp điều chỉnh bó dựa trên mô hình đã khắc phục triệt để nhược điểm này bằng cách thay thế hàng nghìn biến tọa độ tự do bằng một số lượng rất nhỏ các hệ số biến dạng thuộc không gian mô hình khuôn mặt. Việc ràng buộc các điểm 3D phải nằm trên bề mặt của mô hình tham số đã thu hẹp đáng kể không gian tìm kiếm, tăng cường độ ổn định số học của hệ phương trình và tạo ra các kết quả tái dựng liền mạch, chân thực hơn hẳn so với phương pháp truyền thống.

### [Slide 8 - Tái dựng từ hai ảnh trực giao]
**Khoa:**  
Chuyển sang hướng tiếp cận thứ hai là tái dựng từ hai ảnh trực giao, thường bao gồm một ảnh chụp chính diện và một ảnh chụp góc nghiêng 90 độ. Phương pháp do Akimoto và cộng sự đề xuất năm 1993 tận dụng triệt để tính chất hình học của hai góc nhìn này: ảnh chính diện cung cấp thông tin tọa độ chiều ngang và chiều cao, trong khi ảnh góc nghiêng cung cấp thông tin chiều sâu chính xác sống mũi và đường viền khuôn mặt. Thông qua một trục trỏ chung là trục chiều cao, hệ thống sẽ ánh xạ và căn chỉnh các điểm đặc trưng giữa hai ảnh, từ đó làm biến dạng một mô hình 3D tham chiếu chung để khớp với đặc điểm hình thái của cá nhân. Ưu điểm lớn nhất của phương pháp này là thuật toán rất đơn giản, tính ổn định cao và đã được ứng dụng thương mại thành công từ rất sớm. Tuy nhiên, điểm hạn chế là trong điều kiện thực tế rất khó để thu thập được hai bức ảnh vuông góc hoàn hảo, đồng thời quy trình vẫn đòi hỏi sự can thiệp căn chỉnh thủ công từ người dùng.

### [Slide 9 - Tái dựng từ một ảnh đơn: Mô hình biến hình]
**Khoa:**  
Trong thực tế triển khai các hệ thống giám sát và nhận dạng, dữ liệu chúng ta có thường chỉ là một bức ảnh 2D duy nhất. Khắc phục thách thức thiếu hụt thông tin chiều sâu này, Blanz và Vetter đã giới thiệu công trình mang tính cách mạng là Mô hình 3D biến hình vào năm 1999. Nhóm nghiên cứu đã số hóa hàng trăm khuôn mặt thực tế bằng máy quét 3D laze để xây dựng hai không gian vectơ độc lập: không gian hình học bề mặt và không gian kết cấu màu da. Một khuôn mặt 3D mới hoàn toàn có thể được biểu diễn bằng sự kết hợp tuyến tính từ các khuôn mặt mẫu trong hai không gian nói trên. Khi chỉ có một ảnh đầu vào, thuật toán phân tích tổng hợp sẽ tìm kiếm các hệ số tổ hợp sao cho hình ảnh hình lăng trụ chiếu 3D xuống mặt phẳng 2D có sự tương đồng lớn nhất với ảnh gốc. Tuy mang lại đột phá lớn, phương pháp này vẫn gặp hạn chế khi khuôn mặt đầu vào có những đặc trưng phân phối màu da hoặc cấu trúc hình thái nằm ngoài tập dữ liệu mẫu ban đầu.

### [Slide 10 - Tái dựng từ một ảnh đơn: Hệ thống tự động]
**Khoa:**  
Một hướng giải quyết khác cho bài toán một ảnh đơn được Liu và cộng sự phát triển năm 2001 hướng đến sự tự động hóa hoàn toàn. Hệ thống tích hợp một mô-đun phát hiện khuôn mặt tự động dựa trên học máy để định vị chính xác vị trí mắt, mũi, miệng mà không cần con người chấm điểm. Ngay sau đó, quá trình khớp mô hình 3D được thực hiện trong không gian tuyến tính dưới phép chiếu trực giao đơn giản hóa. Mặc dù phép chiếu trực giao từ một ảnh không thể cung cấp thông tin chiều sâu hoàn hảo tuyệt đối như quét laze, nhưng nó tạo ra độ chính xác hình học hoàn toàn chấp nhận được tại các góc xoay trung bình. Quan trọng hơn, nhờ khai thác không gian tham số có cấu trúc, hệ thống này mở ra khả năng tạo sinh các biểu cảm khuôn mặt mới ngay trực tiếp trên mô hình 3D vừa tái dựng một cách tự động.

### [Slide 11 - Kết quả tái dựng từ một ảnh đơn]
**Khoa:**  
Trên slide là minh họa kết quả thực nghiệm từ hệ thống tự động của Liu và các cộng sự. Ở hình bên trái, chúng ta có thể thấy từ một bức ảnh chụp 2D duy nhất ban đầu, mô hình 3D cá nhân hóa đã được khôi phục thành công và có thể xoay quan sát dưới nhiều góc độ quang học khác nhau. Hình bên phải cho thấy sức mạnh của việc biểu diễn trong không gian tuyến tính: sau khi có được mô hình 3D trung lập, hệ thống có thể dễ dàng cộng gộp các metric biến dạng biểu cảm để tạo ra các trạng thái tươi cười hay ngạc nhiên vô cùng sinh động.  

Những kỹ thuật mô hình hóa cấu trúc hình học này chính là tiền đề để chúng ta có thể thực hiện thao túng ánh sáng trên bề mặt khuôn mặt. Sau đây, mình xin nhường lại cho bạn Huỳnh Mạnh Tường trình bày phần tiếp theo: Chiếu sáng lại khuôn mặt.

---

## PHẦN 2: CHIẾU SÁNG LẠI KHUÔN MẶT
**Người trình bày:** Huỳnh Mạnh Tường  
**Thời lượng dự kiến:** 8 phút

### [Slide 13 - Chiếu sáng lại khuôn mặt: Tổng quan]
**Tường:**  
Xin cảm ơn Khoa. Mình là Huỳnh Mạnh Tường, và sau đây mình xin tiếp tục bài thuyết trình với nội dung thứ hai: **Chiếu sáng lại khuôn mặt**.  
Trong bài toán nhận dạng khuôn mặt trong tự nhiên, sự biến thiên về hướng và cường độ chiếu sáng của môi trường luôn là nguyên nhân hàng đầu gây suy giảm độ chính xác của các mô hình, thậm chí ảnh hưởng lớn hơn cả sự thay đổi định danh giữa hai người khác nhau. Mục tiêu cốt lõi của kỹ thuật chiếu sáng lại là tổng hợp ra những bức ảnh khuôn mặt dưới các điều kiện chiếu sáng tùy ý từ một hoặc vài bức ảnh ban đầu, trong khi vẫn bảo toàn tuyệt đối đặc điểm hình thái của cá nhân. Trong chương sách này, chúng ta sẽ đi sâu vào hai kỹ thuật nền tảng mang tính ứng dụng cao nhất là kỹ thuật ảnh tỷ lệ và kỹ thuật khai triển Spherical Harmonics. Cả hai phương pháp này đóng vai trò là công cụ tiền xử lý để chuẩn hóa ánh sáng về điều kiện chuẩn, đồng thời là phương pháp tăng cường dữ liệu hiệu quả nhất cho các hệ thống nhận dạng.

### [Slide 14 - Kỹ thuật ảnh tỷ lệ]
**Tường:**  
Kỹ thuật đầu tiên là ảnh tỷ lệ do Riklin-Raviv và Shashua đề xuất năm 2001, được xây dựng dựa trên nguyên lý định luật phản xạ Lambertian. Theo định luật này, cường độ điểm ảnh bằng tích của hệ số phản xạ bề mặt albedo và tích vô hướng giữa vectơ pháp tuyến bề mặt với hướng nguồn sáng. Giả sử chúng ta có hai khuôn mặt của hai cá nhân khác nhau nhưng có cùng cấu trúc pháp tuyến bề mặt 3D, khi lập tỷ số cường độ điểm ảnh giữa hai khuôn mặt này dưới cùng một nguồn sáng, thành phần hướng sáng và pháp tuyến sẽ hoàn toàn bị triệt tiêu, chỉ còn lại tỷ lệ giữa hai hệ số albedo. Điều này dẫn đến một tính chất bất biến vô cùng quan trọng: tỷ lệ cường độ giữa hai khuôn mặt là hằng số không phụ thuộc vào nguồn sáng chiếu vào chúng. Dựa vào công thức trên slide, chúng ta có thể mượn thông tin chiếu sáng của một người tham chiếu đã biết để đắp sang khuôn mặt của một người mới hoàn toàn. Nhược điểm của kỹ thuật này là đòi hỏi phải có một cơ sở dữ liệu ảnh tham chiếu được chụp dưới nhiều điều kiện chiếu sáng chuẩn xác trong phòng thí nghiệm.

### [Slide 15 - Thay đổi ánh sáng từ một ảnh đơn: Spherical Harmonics]
**Tường:**  
Để vượt qua giới hạn phải cần bộ ảnh tham chiếu phức tạp, Wen và các cộng sự năm 2003 đã có một bước đột phá khi áp dụng lý thuyết Spherical Harmonics để thay đổi ánh sáng chỉ từ một ảnh đầu vào duy nhất. Nhóm nghiên cứu đã chứng minh về mặt toán học rằng hàm cường độ bức xạ trên đối tượng Lambertian có thể được xấp xỉ cực kỳ chính xác chỉ bằng 9 hàm cơ sở Spherical Harmonics bậc thấp. Đặc biệt hơn, nghiên cứu phân tích tính chất vật lý của da mặt con người và phát hiện ra rằng năng lượng phản xạ chủ yếu tập trung ở thành phần hệ số phản xạ trung bình, các thành phần biến thiên tần số cao gần như triệt tiêu. Nhờ phát hiện này, bài toán khôi phục ánh sáng từ một ảnh được chuyển hóa về việc giải hệ phương trình bình phương tối thiểu tuyến tính để ước lượng 9 tham số chiếu sáng. Kết quả thu được cho phép tách thành công bản đồ bức xạ ra khỏi ảnh gốc mà không cần bất kỳ thông tin hình học 3D tiên nghiệm nào.

### [Slide 16 - Ứng dụng chiếu sáng lại khuôn mặt]
**Tường:**  
Sức mạnh của kỹ thuật Spherical Harmonics được thể hiện rõ nét qua ứng dụng thay đổi ánh sáng khuôn mặt. Khi khuôn mặt con người di chuyển, vectơ pháp tuyến tại mỗi điểm ảnh sẽ thay đổi theo hướng xoay mới. Hệ thống chỉ cần tính toán lại giá trị của 9 hàm cơ sở Spherical Harmonics tại các hướng pháp tuyến mới để cập nhật cường độ ánh sáng một cách liên tục theo thời gian thực. Như chúng ta thấy trên hình minh họa của Wen và cộng sự, ảnh tổng hợp ở hàng dưới có hiệu ứng chiếu sáng, vùng sáng và vùng tối chuyển dịch cực kỳ khớp với ảnh chụp thực tế ở hàng trên. Những sai khác rất nhỏ chỉ xuất hiện ở các điểm phản xạ gương trên đỉnh mũi hay trán, vì da người thực tế có tính chất phản xạ lai tạp phức tạp hơn lý thuyết Lambertian thuần túy.

### [Slide 17 - Chỉnh sửa chiếu sáng]
**Tường:**  
Không chỉ dừng lại ở việc khôi phục và di chuyển nguồn sáng hiện có, kỹ thuật Spherical Harmonics còn cho phép chúng ta chủ động chỉnh sửa và thiết kế môi trường chiếu sáng mới cho khuôn mặt. Do toàn bộ hiệu ứng ánh sáng được tham số hóa thành 9 hệ số của hàm cơ sở, người điều khiển chỉ cần thay đổi giá trị của các hệ số này là có thể tạo ra các hiệu ứng hình ảnh đa dạng. Chúng ta có thể bổ sung các nguồn sáng ảo để tạo bóng đổ nghệ thuật, thay đổi góc chiếu từ trái sang phải, từ trên xuống dưới, hoặc thậm chí mô phỏng thay đổi sắc độ màu sáng của môi trường xung quanh như ánh sáng tím hoàng hôn hay ánh vàng đèn sân khấu. Khả năng chỉnh sửa linh hoạt này mở ra một hướng đi đầy tiềm năng để tự động hóa việc sinh ra các tập dữ liệu huấn luyện đa dạng về độ sáng, giúp các mô hình học sâu sau này không bị học tủ vào một điều kiện môi trường cụ thể.

### [Slide 18 - Ứng dụng cho nhận dạng khuôn mặt]
**Tường:**  
Để chứng minh giá trị thực tiễn của chiếu sáng lại trong bài toán nhận dạng, Qing và các cộng sự năm 2004 đã xây dựng một quy trình tiền xử lý chuẩn hóa ánh sáng đầy ấn tượng. Khi một bức ảnh khuôn mặt với ánh sáng phức tạp, lệch góc hoặc bóng đổ sâu được đưa vào hệ thống, thuật toán sẽ ước lượng 9 hệ số Spherical Harmonics của bức ảnh đó. Để đưa khuôn mặt về trạng thái chuẩn hóa quang học hoàn hảo nhất, hệ thống tiến hành triệt tiêu toàn bộ 8 hệ số chiếu sáng có hướng, chỉ giữ lại duy nhất hệ số hằng số trung bình phản ánh ánh sáng khuếch tán đồng nhất. Tiếp đó, kỹ thuật ảnh tỷ lệ được áp dụng trên ảnh đã chuẩn hóa để đối sánh với cơ sở dữ liệu. Thử nghiệm trên tập dữ liệu chuẩn PIE đã chứng minh rằng việc áp dụng quy trình tiền xử lý này giúp cải thiện vượt bậc độ chính xác nhận dạng, đưa hệ thống đạt độ bền vững gần như tuyệt đối trước mọi thử thách về môi trường chiếu sáng.  

Như vậy, qua hai nội dung đầu tiên, chúng ta đã nắm bắt được cách mô hình hóa hình thái 3D và điều khiển ánh sáng trên khuôn mặt theo lý thuyết truyền thống. Sau đây, mình xin chuyển lời lại cho bạn Đạt để trình bày về hướng Tổng hợp biểu cảm khuôn mặt cũng như nghiên cứu tiên tiến SOTA SynFER.

---

## PHẦN 3: TỔNG HỢP BIỂU CẢM KHUÔN MẶT, NGHIÊN CỨU SOTA SYNFER & THỰC NGHIỆM
**Người trình bày:** Đàm Tiến Đạt  
**Thời lượng dự kiến:** 9 phút lời thoại + 3 phút demo video

### [Slide 20 - Tổng hợp biểu cảm khuôn mặt: Tổng quan]
**Đạt:**  
Xin cảm ơn Tường. Mình xin phép được tiếp tục bài thuyết trình với nội dung thứ ba: **Tổng hợp biểu cảm khuôn mặt**.  
Nếu mô hình hóa hình học và chiếu sáng xây dựng nên phần tĩnh của một cấu trúc khuôn mặt, thì tổng hợp biểu cảm chính là chìa khóa thổi hồn vào cấu trúc đó, tạo ra những chuyển động trạng thái cảm xúc sống động như con người. Trong giáo trình, bài toán tổng hợp biểu cảm được phân chia thành ba hướng tiếp cận kinh điển: phương pháp mô phỏng vật lý hệ cơ xương, phương pháp nội suy biến hình hình học và phương pháp ánh xạ biểu cảm từ diễn viên. Đây là nền tảng cốt lõi cho mọi ứng dụng giao tiếp trực quan, từ công nghiệp hoạt hình cho đến thiết kế giao diện tương tác người máy thế hệ mới.

### [Slide 21 - Dựa trên vật lý & Biến hình]
**Đạt:**  
Đi sâu vào hai hướng tiếp cận đầu tiên, phương pháp dựa trên vật lý do Terzopoulos và cộng sự phát triển năm 1990 nỗ lực mô phỏng cơ chế giải phẫu sinh học của con người. Bề mặt da mặt được mô hình hóa thành một mạng lưới khối lượng và lò xo nhiều lớp, chịu lực kéo đàn hồi từ hai nhóm cơ chính là cơ tuyến tính và cơ vòng. Khi kích hoạt lực co cơ, mạng lưới tự động biến dạng theo quy luật cơ học. Tuy có cơ sở khoa học chặt chẽ, phương pháp này gặp hạn chế lớn khi không thể tái hiện được các chi tiết vi mô phức tạp như các nếp nhăn mảnh trên trán hay vết chân chim quanh mắt, đồng thời chi phí tính toán giải tích là cực kỳ tốn kém.  

Trái ngược với tính chất tính toán nặng nề của mô phỏng vật lý, phương pháp biến hình của Pighin và cộng sự năm 1998 tiếp cận theo hướng dữ liệu trực quan. Phương pháp này thu thập một tập mẫu các khuôn mặt với các biểu cảm cơ bản đã được căn chỉnh 3D, sau đó thực hiện tổ hợp tuyến tính lồi để pha trộn trạng thái. Nhờ tính toán đơn giản, phương pháp biến hình cho ra ảnh tổng hợp rất sắc nét trên các góc nhìn chuẩn. Tuy nhiên, điểm yếu là không gian biểu cảm sinh ra bị giới hạn hoàn toàn trong khuôn khổ của tập mẫu có sẵn, và rất dễ xảy ra hiện tượng bóng ma hoặc méo mó hình học tại các vùng ranh giới có sự thay đổi cấu trúc lớn giữa cười và giận dữ.

### [Slide 22 - Ánh xạ biểu cảm: Ảnh tỉ số biểu cảm]
**Đạt:**  
Để giải quyết bài toán tái hiện nếp nhăn động mà không cần giải lập phương trình vật lý phức tạp, Liu và các cộng sự năm 2001 đã đề xuất một giải pháp cực kỳ thông minh là Expression Ratio Image (ERI - Ảnh tỉ số biểu cảm). Nhóm tác giả nhận xét rằng khi một người diễn xuất thể hiện cảm xúc, sự biến đổi trên khuôn mặt bao gồm hai thành phần: sự dịch chuyển hình học tổng thể và sự thay đổi chiếu sáng cục bộ do nếp nhăn da tạo ra. Bằng cách lấy tỷ số cường độ điểm ảnh giữa bức ảnh biểu cảm và bức ảnh trung lập của cùng một người diễn viên, toàn bộ thông tin màu da trung lập sẽ bị loại bỏ, chỉ trích xuất lại duy nhất bản đồ ánh sáng nếp nhăn. Khi nhân bản đồ tỷ số này với ảnh khuôn mặt trung lập của một người mới bất kỳ sau khi đã căn chỉnh hình học, chúng ta có thể truyền tải trọn vẹn chi tiết nếp nhăn sống động sang người mới mà không bị lẫn màu da hay định danh của diễn viên ban đầu.

### [Slide 23 - Kết quả ánh xạ chi tiết bằng ERI]
**Đạt:**  
Sự vượt trội của phương pháp Expression Ratio Image được minh chứng rõ ràng qua đối sánh thực nghiệm trên slide. Ở hình giữa là kết quả khi chúng ta chỉ sử dụng biến dạng bẻ cong hình học thuần túy: khu vực trán và quanh mắt của nhân vật chỉ bị giãn ra hoặc co lại theo lưới điểm, hoàn toàn phẳng lì và thiếu đi cảm giác sinh học thực tế. Ngược lại, ở hình bên phải, khi được tích hợp ERI, các đường nếp nhăn gấp khúc trên trán, sự co rụt cơ mi và vùng tối quanh khóe miệng xuất hiện cực kỳ tự nhiên, khiến bức ảnh tổng hợp có độ chân thực rất cao. Hạn chế duy nhất của kỹ thuật này là hệ thống luôn phụ thuộc vào việc phải có sẵn một bộ ảnh chụp biểu cảm nguồn chất lượng cao từ diễn viên diễn xuất thực tế.

### [Slide 24 - Ứng dụng ERI lên tranh và tượng]
**Đạt:**  
Tính đa năng và uyển chuyển của kỹ thuật Expression Ratio Image đã mở ra những ứng dụng sáng tạo vượt ra ngoài phạm vi khuôn mặt người thật. Nhóm nghiên cứu của Liu đã thử nghiệm áp dụng phương pháp này để thao túng biểu cảm trên các tác phẩm nghệ thuật lịch sử. Như chúng ta thấy trên hình bên trái, kiệt tác hội họa Mona Lisa với nụ cười bí ẩn nguyên bản đã được thổi hồn để thể hiện các cảm xúc ngạc nhiên, buồn bã hay cười rạng rỡ một cách vô cùng thuyết phục. Tương tự ở hình bên phải, các bức tượng điêu khắc đá cổ kính hay tượng thạch cao vô tri vô giác cũng được ánh xạ thành công các biểu cảm sống động. Kết quả này chứng minh rằng ERI thực sự đã phân tách và mô hình hóa thành công bản chất quang học của chuyển động nếp nhăn độc lập với chất liệu bề mặt.

### [Slide 25 - Tổng hợp điều khiển bằng hình học]
**Đạt:**  
Để khắc phục điểm yếu phụ thuộc vào ảnh nguồn của người diễn xuất trong kỹ thuật ERI, Zhang và cộng sự năm 2003 đã phát triển một kiến trúc mới: hệ thống tổng hợp biểu cảm điều khiển bằng hình học. Trong hệ thống này, người dùng hoặc hệ thống điều khiển chỉ cần cung cấp quỹ đạo dịch chuyển của các điểm đặc trưng hình học cơ bản trên khuôn mặt, chẳng hạn như chuyển động kéo mép hay rướn mày. Thuật toán được xây dựng trên giả định rằng không gian biểu cảm bao gồm sự đồng biến giữa hình học và kết cấu trong một tập tổ hợp lồi. Khi nhận được một bộ điểm hình học mới, hệ thống tiến hành chiếu bộ điểm này vào không gian mẫu để tìm kiếm bộ hệ số tổ hợp tối ưu nhất. Từ bộ hệ số đó, thuật toán lập tức nội suy và tổng hợp ra lớp kết cấu biểu cảm tương ứng. Phương pháp này cho phép điều khiển khuôn mặt linh hoạt thông qua các tham số hình học mức cao mà không cần lưu trữ hay quay chụp ảnh diễn viên cho từng trường hợp.

---

### [Slide 27 - Động lực và Ý tưởng cốt lõi của SynFER]
**Đạt:**  
Kính thưa thầy cô và các bạn, những phương pháp chúng ta vừa tìm hiểu trong Chương 20 mang lại cái nhìn sâu sắc về mặt lý thuyết hình học và quang học. Tuy nhiên, khi ứng dụng vào các bài toán học sâu hiện đại như Facial Expression Recognition (FER - Nhận dạng biểu cảm khuôn mặt), các mô hình truyền thống bộc lộ nhược điểm là không thể tạo ra sự đa dạng vô tận về góc chụp, ánh sáng và bối cảnh. Để vượt qua rào cản này, nhóm chúng em đã lựa chọn nghiên cứu và thực nghiệm bài báo tiên tiến SOTA vừa được công bố với tiêu đề: *SynFER: Towards Boosting Facial Expression Recognition with Synthetic Data*.  

Động lực chính của nghiên cứu xuất phát từ thực trạng là các mô hình học sâu FER hiện nay vô cùng khát dữ liệu huấn luyện chất lượng cao, nhưng công tác thu thập ảnh biểu cảm thực tế trong tự nhiên lại rủi ro về quyền riêng tư và cực kỳ tốn kém chi phí gán nhãn thủ công, chưa kể nhãn gán thường bị sai lệch do cảm nhận chủ quan của con người. Ý tưởng cốt lõi của tác giả là xây dựng một quy trình tổng hợp dữ liệu khổng lồ dựa trên Diffusion model. SynFER cho phép tạo ra số lượng không giới hạn các bức ảnh biểu cảm mới với độ chân thực tuyệt đối, được gán nhãn chuẩn xác tự động nhờ cơ chế kiểm soát kép bằng các Action Unit cơ mặt và Semantic Guidance.

### [Slide 28 - Nền tảng Toán học Mô hình Diffusion]
**Đạt:**  
Để hiểu được kiến trúc SynFER, chúng ta cần lướt qua nền tảng toán học của Diffusion model. Khác với biến hình hình học truyền thống, Diffusion model hoạt động theo nguyên lý nhiệt động lực học thống kê thông qua hai quá trình ngược nhau. Quá trình thuận là một chuỗi Markov thực hiện tiêm dần nhiễu Gaussian vào một bức ảnh sạch ban đầu qua $T$ bước thời gian cho đến khi ảnh biến hoàn toàn thành nhiễu trắng ngẫu nhiên theo phương trình 23. Quá trình nghịch là quá trình học cách khử nhiễu: một mạng thần kinh sâu được huấn luyện để dự đoán và loại bỏ lượng nhiễu đã thêm vào ở từng bước thời gian theo phương trình 24. Hàm mất mát tối ưu hóa cho mạng là bình phương khoảng cách giữa nhiễu thực tế và nhiễu do mô hình dự đoán. Khi mô hình đã hội tụ, chúng ta chỉ cần lấy một mẫu nhiễu ngẫu nhiên và đưa qua chuỗi khử nhiễu có điều kiện là có thể kiến tạo nên một bức ảnh hoàn toàn mới chưa từng tồn tại trên đời.

### [Slide 29 - Sơ đồ Pipeline của SynFER]
**Đạt:**  
Trên slide là sơ đồ kiến trúc tổng thể của hệ thống SynFER được tác giả đề xuất. Để có được một mô hình tạo sinh biểu cảm chuẩn xác, quy trình được vận hành qua ba trụ cột chính. Đầu tiên là giai đoạn chuẩn bị dữ liệu với việc xây dựng tập bộ dữ liệu lai ghép quy mô lớn FEText để cung cấp tri thức phong phú cho mô hình tạo sinh. Thứ hai là mô-đun điều khiển không gian cho phép tiêm chính xác các vị trí và cường độ cử động cơ mặt vào quá trình sinh ảnh thông qua một mạng thích ứng. Thứ ba là cơ chế Semantic Guidance tích cực trong quá trình khử nhiễu, tác động lực kéo gradient hướng đích để ép hình ảnh sinh ra phải thể hiện rõ nét nhãn biểu cảm mục tiêu mà không bị mơ hồ hay trung lập.

### [Slide 30 - Các kỹ thuật chi tiết trong SynFER]
**Đạt:**  
Đi sâu vào chi tiết kỹ thuật của ba trụ cột nói trên:
- **Thứ nhất là tập dữ liệu lai ghép FEText:** Tác giả nhận thấy các bộ dữ liệu hiện có rất rời rạc, bộ thì có độ phân giải cao nhưng thiếu nhãn chi tiết, bộ thì có nhãn nhưng ảnh mờ. Nhóm nghiên cứu đã hợp nhất các bộ dữ liệu chất lượng nhất, chuẩn hóa độ phân giải, khử nhiễu ảnh và sử dụng Mô hình ngôn ngữ lớn đa phương thức để tự động trích xuất mô tả văn bản giàu ngữ nghĩa cho từng khuôn mặt, tạo ra tập dữ liệu FEText vượt trội cả về chất lượng lẫn số lượng.
- **Thứ hai là kiểm soát bằng Action Unit:** Trong chuẩn hệ thống mã hóa cử động khuôn mặt FACS, mỗi chuyển động cơ được quy định thành một Action Unit. SynFER không dùng vectơ tham số thô mà ánh xạ các cường độ Action Unit này thành các bản đồ đặc trưng không gian. Bản đồ này được đưa vào mạng tạo sinh thông qua cơ chế Decoupled Cross-Attention (chú ý chéo tách biệt với văn bản), giúp mô hình biết chính xác cần co cơ ở vị trí nào trên khuôn mặt.
- **Thứ ba là Semantic Guidance trong quá trình khử nhiễu:** Để giải quyết triệt để tình trạng ảnh sinh ra bị nhẹ đô hoặc thiếu cảm xúc, tác giả tích hợp một bộ phân lớp biểu cảm phụ trợ vào quy trình khử nhiễu. Tại mỗi bước thời gian, ảnh dự đoán sạch $\hat{x}_0$ được đánh giá hàm mất mát phân lớp $\mathcal{L}_g$. Gradient ngược từ hàm mất mát này được trực tiếp cộng dồn để cập nhật text embedding điều kiện theo phương trình 55. Cơ chế này giống như một người thầy liên tục uốn nắn Diffusion model phải vẽ nét mặt đậm hơn, rõ hơn đúng với cảm xúc mục tiêu.

### [Slide 32 - Đối chiếu phương pháp truyền thống và hiện đại]
**Đạt:**  
Đặt lên bàn cân so sánh giữa kiến thức trong Chương 20 của giáo trình và bài báo tiên tiến SynFER, chúng ta nhận thấy những giá trị kế thừa và sự tiến hóa vượt bậc:
- **Về điểm tương đồng cốt lõi:** Cả lý thuyết giáo trình và SOTA đều chia sẻ một hệ tư tưởng nền tảng là: biểu cảm khuôn mặt con người là kết quả trực tiếp của các chuyển động cơ mặt cục bộ. Các nhóm cơ tuyến tính và cơ vòng được mô phỏng bằng hệ lò xo trong sách giáo khoa năm 1990 chính là tiền thân về mặt ý tưởng cho các Action Unit trong SynFER ngày nay.
- **Về sự tiến hóa kỹ thuật:** Phương pháp truyền thống tác động biến đổi trực tiếp lên các điểm ảnh gốc hoặc làm biến dạng lưới hình học. Cách làm này bị giới hạn vật lý rất lớn: nếu khuôn mặt mục tiêu có góc xoay lớn hoặc cấu trúc da khác biệt, lưới điểm sẽ bị rách, tạo lỗi bóng ma và vùng biên bị méo mó. Ngược lại, SynFER theo cách tiếp cận hiện đại không chỉnh sửa trên ảnh cũ mà sinh ra bức ảnh hoàn toàn mới từ không gian nhiễu dựa trên học tập phân phối xác suất. Nhờ đó, SynFER tái hiện trọn vẹn sự tương tác quang học phức tạp nhất như sự xuất hiện nếp nhăn động, bóng đổ vi mô dưới hốc mắt hay thay đổi sắc mặt mà không gặp bất kỳ giới hạn nào về lưới hình học.

### [Slide 33 - Quá trình Thực nghiệm & Đánh giá]
**Đạt:**  
Để kiểm chứng thực tế tính đúng đắn của bài báo, nhóm chúng em đã bắt tay vào triển khai thực nghiệm trên mã nguồn. Thách thức lớn nhất mà nhóm gặp phải là tác giả bài báo gốc không cung cấp sẵn các trọng số mô hình đã huấn luyện, đồng thời một số cấu hình siêu tham số và chi tiết đánh giá không được mô tả đầy đủ trong bài báo.  
Không nản lòng trước khó khăn, nhóm chúng em đã tự thiết lập hệ thống tính toán trên 2 GPU NVIDIA A100 dung lượng 40GB, tự viết mã nguồn chuẩn bị dữ liệu và tiến hành huấn luyện từ đầu: fine-tune LoRA cho mô hình Stable Diffusion v1.5 trong 5 epochs và huấn luyện Action Unit Adapter trong 5 epochs.  
Đặc biệt hơn, để đạt **điểm thưởng (criterion No. 6)** của đồ án, nhóm chúng em đã tiến hành mở rộng thực nghiệm: đem mô hình SynFER vừa huấn luyện để đánh giá tính tổng quát hóa trên bộ dữ liệu KDEF. Đây là bộ dữ liệu có phân phối hình ảnh hoàn toàn khác biệt nằm ngoài bài báo gốc, giúp kiểm chứng năng lực thích nghi của mô hình trên các đối tượng mới.

### [Slide 34 - Kết quả Thực nghiệm và So sánh]
**Đạt:**  
Trên slide là bảng số liệu tổng hợp kết quả thực nghiệm của nhóm trên hai bộ dữ liệu AffectNet và KDEF, đối chiếu trực tiếp với các phương pháp cơ sở và con số báo cáo trong bài báo gốc thông qua bốn độ đo chuẩn: FID, FER Acc, HPSv2 và MPS.  
Nhìn vào bảng số liệu, điểm nổi bật nhất là độ đo FER Acc của nhóm đạt mức cực kỳ cao: 88.90% trên AffectNet và 95.81% trên KDEF, vượt trội so với con số 55.14% của bài báo gốc. Nguyên nhân của hiện tượng này là trong quá trình suy luận có Semantic Guidance, hệ thống sử dụng mạng phân loại POSTER\_V2 để tối ưu hóa hướng sinh ảnh. Việc sử dụng trùng lặp chính mạng POSTER\_V2 làm giám khảo đánh giá FER Acc ở khâu cuối đã dẫn đến hiện tượng tối ưu hóa quá mức (over-optimization), khiến điểm số phân loại đạt ngưỡng rất cao.  
Đối với hai chỉ số FID và MPS đánh giá độ chân thực quang học, kết quả của nhóm cao hơn bài báo gốc do mô hình chỉ được fine-tune trong 5 epochs trên nguồn tài nguyên máy tính hạn chế, chưa đạt độ hội tụ tuyệt đối. Tuy nhiên, chỉ số HPSv2 đánh giá chất lượng nhận thức của con người vẫn đạt 0.271 trên AffectNet và 0.272 trên KDEF, tương đương với các phương pháp hiện đại như PlayGround hay FineFace, chứng minh năng lực sinh biểu cảm sắc nét và giữ định danh rất tốt của cấu trúc SynFER.

### [Slide 35 - Đánh giá ưu nhược điểm và Đề xuất cải tiến]
**Đạt:**  
Từ quá trình nghiên cứu và chạy thực nghiệm thực tế, nhóm chúng em xin đưa ra những đánh giá khách quan về mô hình SynFER:
- **Về ưu điểm:** SynFER đã giải quyết triệt để vấn đề rách lưới và méo dạng hình học của các phương pháp truyền thống; có khả năng tạo ra nguồn dữ liệu huấn luyện vô hạn với nhãn gán chuẩn xác; đồng thời bảo toàn định danh khuôn mặt gốc cực kỳ ấn tượng.
- **Về hạn chế:** Do quy trình phụ thuộc vào các bước trung gian, nếu công cụ trích xuất Action Unit ban đầu nhận diện sai cơ mặt trên ảnh gốc, lỗi đó sẽ bị khuếch đại trong ảnh sinh ra. Ngoài ra, bản chất lặp 50 bước của Diffusion model khiến tốc độ sinh ảnh còn chậm, khó áp dụng cho các ứng dụng thời gian thực.
- **Đề xuất cải tiến:** Để khắc phục hạn chế về tốc độ, nhóm đề xuất tích hợp kiến trúc Latent Consistency Models (LCM) hoặc SDXL Turbo vào quy trình SynFER, giúp thu gọn quá trình khử nhiễu từ 50 bước xuống chỉ còn từ 4 đến 8 bước, tăng tốc độ sinh ảnh gấp hàng chục lần. Bên cạnh đó, nhóm đề xuất mở rộng kiến trúc bằng cách bổ sung mô-đun Temporal Attention vào mạng Diffusion, nâng cấp SynFER từ việc chỉ sinh ảnh tĩnh riêng lẻ lên khả năng tạo sinh các đoạn video hoạt hình biểu cảm chuyển động liền mạch theo chuỗi thời gian.

---

### [Slide 37 - Demo Ứng dụng & Video thực nghiệm]
**Đạt:**  
Để thầy cô và các bạn có cái nhìn trực quan và sinh động nhất về toàn bộ quy trình hoạt động của SynFER cũng như những kết quả mà nhóm chúng em đã thực nghiệm, sau đây nhóm xin mời thầy cô và các bạn cùng hướng mắt lên màn hình để theo dõi video demo minh họa hệ thống có thời lượng 3 phút đã được nhóm quay và chuẩn bị sẵn.

*(--- BẬT VIDEO DEMO MINH HỌA - THỜI LƯỢNG 3 PHÚT ---)*  
*(Trong khi video phát, Đạt có thể thuyết minh phụ họa theo diễn biến video: "Như thầy cô đang thấy trên màn hình là giao diện hệ thống thực nghiệm của nhóm. Chúng em tải lên một khuôn mặt trung lập ban đầu. Tiếp theo, ở bảng điều khiển bên phải, chúng em thay đổi cường độ của Action Unit số 12 là cơ kéo mép miệng và số 6 là cơ mi mắt để mô phỏng nụ cười hạnh phúc rạng rỡ. Khi kích hoạt quá trình khử nhiễu có Semantic Guidance, chỉ sau vài giây tính toán, mô hình SynFER đã sinh ra bốn bức ảnh biểu cảm mới với độ sắc nét tuyệt đối, nếp nhăn đuôi mắt xuất hiện cực kỳ chân thực và hoàn toàn giữ đúng khuôn mặt của người ban đầu. Tiếp tục kiểm chứng ảnh vừa sinh bằng mô hình nhận dạng, hệ thống cho ra xác suất độ tự tin với lớp Hạnh phúc lên tới 98.5%...")*

*(--- KẾT THÚC VIDEO DEMO ---)*

**Đạt:**  
Video demo vừa rồi cũng đã khép lại phần trình bày đồ án môn học Nhận dạng của nhóm chúng em. Nhóm chúng em xin chân thành cảm ơn thầy cô và các bạn đã chú ý lắng nghe. Nhóm rất mong nhận được những nhận xét, ý kiến đóng góp cũng như các câu hỏi từ thầy cô và các bạn để đồ án của nhóm được hoàn thiện hơn. Em xin trân trọng cảm ơn!

---

## PHẦN 4: CÂU HỎI THẢO LUẬN VÀ CHUẨN BỊ VẤN ĐÁP (Q&A PREPARATION)
*(Tài liệu này tổng hợp 11 câu hỏi chuyên sâu xoay quanh lý thuyết Chương 20, bài báo SOTA SynFER và quá trình thực nghiệm của nhóm, kèm theo câu trả lời học thuật chuẩn xác, hỗ trợ nhóm tự tin đạt điểm tối đa trong phần Vấn đáp - 15% của đồ án).*

### Câu hỏi 1: Sự khác biệt bản chất giữa thuật toán giải lặp ICP trong mô hình 3DMM và kỹ thuật Điều chỉnh bó dựa trên mô hình là gì? Tại sao Điều chỉnh bó lại cho độ ổn định cao hơn?
**Trả lời:**  
- Trong thuật toán giải lặp ICP thông thường, quá trình tối ưu được tách thành hai bước rời rạc: cố định tham số hình học để giải chuyển động camera, rồi ngược lại cố định camera để giải tham số hình học. Việc tách rời này dễ dẫn đến hiện tượng dao động hoặc mắc kẹt tại các cực trị cục bộ khi ảnh đầu vào có nhiễu hoặc góc quay quá lớn.
- Ngược lại, kỹ thuật Điều chỉnh bó dựa trên mô hình gộp chung cả tham số chuyển động camera và tham số hình học mô hình vào một hàm mục tiêu tối ưu duy nhất. Quá trình giải đồng thời giúp các biến hỗ trợ ràng buộc lẫn nhau. Đặc biệt, vì các điểm 3D buộc phải nằm trên bề mặt mô hình tham số hóa thay vì là các biến tự do trong không gian, số lượng biến tối ưu giảm từ hàng nghìn xuống chỉ còn vài chục tham số. Điều này giúp không gian nghiệm nhỏ hơn, ma trận thông tin ổn định số học hơn và kết quả tái dựng chính xác, liền mạch hơn.

### Câu hỏi 2: Spherical Harmonics là gì? Tại sao công cụ toán học này lại được ứng dụng trong chiếu sáng lại khuôn mặt?
**Trả lời:**  
- **Spherical Harmonics** (các hàm điều hòa hình cầu) là tập hợp các hàm cơ sở trực giao được định nghĩa trên bề mặt của một hình cầu 3D, đóng vai trò trong không gian góc tương tự như biến đổi Fourier đối với tín hiệu theo thời gian. Bất kỳ một hàm số liên tục nào được định nghĩa trên mặt cầu đều có thể được phân tích và biểu diễn thành chuỗi tổng tuyến tính của các hàm cơ sở Spherical Harmonics với các tần số góc từ thấp đến cao (được chỉ số hóa bởi bậc $l$ và bậc phụ $m$).
- Trong thị giác máy tính và bài toán chiếu sáng lại khuôn mặt (Face Relighting), ánh sáng môi trường từ mọi hướng chiếu vào một điểm trên bề mặt da có thể được mô hình hóa như một hàm số bức xạ trên mặt cầu. Nhờ khai triển Spherical Harmonics, tác giả có thể tham số hóa toàn bộ môi trường ánh sáng phức tạp vô hạn thành một tập vectơ hệ số nhỏ gọn. Do bề mặt da người phản xạ khuếch tán theo định luật Lambertian (đóng vai trò như một bộ lọc thông thấp), các thành phần tần số cao bị triệt tiêu, giúp chỉ cần 9 hàm cơ sở bậc thấp nhất ($l \le 2$) là đã đủ để xấp xỉ chính xác tới 99% trường ánh sáng bức xạ trên khuôn mặt.

### Câu hỏi 3: Tại sao trong kỹ thuật Spherical Harmonics cho chiếu sáng lại khuôn mặt, tác giả chỉ sử dụng 9 hàm cơ sở bậc thấp ($l \le 2$) mà không sử dụng các bậc cao hơn để tăng độ chi tiết?
**Trả lời:**  
- Việc chỉ sử dụng 9 hàm cơ sở bậc thấp xuất phát từ tính chất phản xạ quang học đặc thù của bề mặt da mặt con người. Theo lý thuyết Lambertian và phân tích thực nghiệm của Ramamoorthi và Hanrahan, cấu trúc da con người đóng vai trò như một bộ lọc thông thấp quang học: ánh sáng môi trường khi chiếu vào da sẽ bị khuếch tán mạnh dưới lớp biểu bì trước khi phản xạ lại.
- Do đó, hơn 99% năng lượng ánh sáng bức xạ trên bề mặt khuôn mặt được tập trung ở các thành phần tần số thấp tương ứng với các hàm Spherical Harmonics từ bậc $l = 0$ đến bậc $l = 2$. Việc tăng lên các bậc cao hơn ($l \ge 3$) không những không mang lại thêm thông tin chiếu sáng có giá trị mà còn làm tăng mức độ nhạy cảm với nhiễu ảnh và bóng đổ sắc nét (cast shadows), đồng thời làm tăng chi phí tính toán khi giải phương trình bình phương tối thiểu.

### Câu hỏi 4: Kỹ thuật ảnh tỷ lệ giải quyết bài toán chuyển ánh sáng giữa hai người như thế nào? Giới hạn lớn nhất khiến phương pháp này khó triển khai trong các ứng dụng thực tế là gì?
**Trả lời:**  
- Kỹ thuật ảnh tỷ lệ dựa trên giả định Lambertian: khi hai khuôn mặt có cấu trúc hình học và pháp tuyến 3D giống nhau, tỷ lệ cường độ giữa hai điểm ảnh tương ứng dưới cùng một nguồn sáng chỉ phụ thuộc vào tỷ lệ hệ số albedo bề mặt mà không phụ thuộc vào cường độ hay hướng sáng. Nhờ tính chất này, ta có thể tính ảnh tỷ lệ từ ảnh tham chiếu, rồi nhân với ảnh của người mục tiêu để tái tạo lại ánh sáng mong muốn.
- Giới hạn lớn nhất của phương pháp này là điều kiện giả định quá khắt khe. Trong thực tế, hình thái khuôn mặt và cấu trúc pháp tuyến của hai người không bao giờ giống nhau hoàn toàn. Do đó, để áp dụng được, hệ thống bắt buộc phải căn chỉnh hình học lưới điểm cực kỳ chính xác giữa hai người. Hơn nữa, phương pháp đòi hỏi phải có một cơ sở dữ liệu ảnh tham chiếu của cùng một người được chụp dưới rất nhiều góc sáng chuẩn trong phòng thí nghiệm, điều gần như bất khả thi trong môi trường nhận dạng tự nhiên không kiểm soát.

### Câu hỏi 5: Phương pháp Ảnh tỉ số biểu cảm khắc phục nhược điểm của mô phỏng vật lý và biến hình hình học như thế nào? Tại sao Ảnh tỉ số biểu cảm lại tái tạo được nếp nhăn da chân thực?
**Trả lời:**  
- Mô phỏng vật lý có chi phí tính toán cực cao và không thể tạo nếp nhăn vi mô, trong khi biến hình hình học bị giới hạn bởi tập mẫu và dễ làm méo ảnh khi chuyển tiếp biểu cảm. Phương pháp Expression Ratio Image (ERI - Ảnh tỉ số biểu cảm) khắc phục điều này bằng cách không cố gắng mô phỏng cơ xương hay bẻ cong pixel, mà tiếp cận từ góc độ chiếu sáng.
- Khi một người thể hiện cảm xúc, da bị co lại tạo ra các nếp gấp. Các nếp gấp này thay đổi vectơ pháp tuyến cục bộ, tạo ra các vi bóng đổ và thay đổi cường độ sáng nhỏ. Tỷ số cường độ giữa ảnh biểu cảm và ảnh trung lập đã loại bỏ hoàn toàn màu da phẳng ban đầu, đóng vai trò như một bộ lọc quang học cô đọng nguyên vẹn thông tin chi tiết về chiều sâu và vi bóng đổ của nếp nhăn. Khi áp tỉ số này lên một khuôn mặt mới, các vi bóng đổ nếp nhăn được hiển thị chính xác trên màu da của người mới, tạo nên độ chân thực sinh học rất cao.

### Câu hỏi 6: Trong kiến trúc của bài báo SynFER, tác giả đã sử dụng Action Unit (FAU) theo chuẩn FACS như thế nào để điều khiển quá trình sinh ảnh thay vì sử dụng nhãn văn bản đơn thuần?
**Trả lời:**  
- Nhãn văn bản đơn thuần như Hạnh phúc hay Giận dữ mang tính trừu tượng rất cao, không cung cấp thông tin hình học về việc cơ mặt nào phải dịch chuyển bao nhiêu, dẫn đến ảnh sinh ra thường bị trung lập hoặc thiếu nhất quán.
- SynFER khai thác hệ thống Action Unit để định lượng chuyển động cơ mặt. Thay vì đưa vectơ giá trị thô vào mạng, SynFER sử dụng Action Unit Adapter ánh xạ cường độ và vị trí các Action Unit thành một bản đồ đặc trưng không gian 2D. Bản đồ này được tiêm vào các lớp của Diffusion model thông qua cơ chế Decoupled Cross-Attention (chú ý chéo tách biệt). Nhờ đó, Diffusion model nhận được chỉ dẫn chính xác trong không gian 2D về khu vực cụ thể cần co cơ, độ rướn mày hay độ kéo khóe miệng, tạo ra biểu cảm chuẩn xác theo quy chuẩn y sinh.

### Câu hỏi 7: Cơ chế Semantic Guidance trong quá trình khử nhiễu của SynFER hoạt động ra sao và đóng vai trò gì trong việc nâng cao độ chính xác của ảnh sinh ra?
**Trả lời:**  
- Trong Diffusion model tiêu chuẩn, dù có điều kiện Action Unit, ảnh sinh ra đôi khi vẫn bị nhẹ đô hoặc không thể hiện rõ đặc trưng phân lớp của biểu cảm mục tiêu do phân phối học bị phân tán.
- SynFER giới thiệu cơ chế Semantic Guidance bằng cách tích hợp một bộ phân lớp biểu cảm phụ trợ đã được huấn luyện vào ngay quá trình khử nhiễu lặp. Tại mỗi bước thời gian của quá trình nghịch, ảnh dự đoán sạch được đưa qua bộ phân lớp để tính hàm mất mát phân lớp so với nhãn mục tiêu. Thuật toán tính toán gradient ngược của hàm mất mát này theo vectơ text embedding điều kiện, và cộng gradient đó vào embedding cho bước lặp tiếp theo. Quá trình này tạo ra lực kéo toán học định hướng Diffusion model phải hội tụ về đúng phân phối quang học có độ tự tin cao nhất đối với nhãn biểu cảm mong muốn.

### Câu hỏi 8: Sự khác biệt lớn nhất giữa việc tạo sinh biểu cảm bằng các phương pháp truyền thống trong Chương 20 so với kiến trúc tạo sinh hiện đại SynFER là gì?
**Trả lời:**  
- Sự khác biệt bản chất nằm ở cơ chế biến đổi điểm ảnh:
  - **Phương pháp truyền thống (Chương 20):** Là phương pháp biến đổi trực tiếp trên ảnh gốc. Chúng sử dụng các thuật toán nội suy hoặc kéo dãn lưới hình học để bẻ cong, dịch chuyển các pixel của ảnh ban đầu sang vị trí mới. Khi mức độ biến dạng lớn hoặc góc mặt thay đổi, cấu trúc lưới bị rách, tạo ra các vùng méo mó phi thực tế và không thể tự sinh ra các vùng kết cấu bị che khuất.
  - **Phương pháp hiện đại (SynFER):** Là phương pháp tái tạo từ đầu. SynFER không dịch chuyển các pixel của bức ảnh cũ. Thay vào đó, mô hình bắt đầu từ một ma trận nhiễu trắng ngẫu nhiên và từng bước khử nhiễu để vẽ ra một bức ảnh mới hoàn toàn dựa trên tri thức phân phối xác suất đã học. Nhờ vậy, SynFER có thể kiến tạo những kết cấu da mới, nếp nhăn động, hay tự động bù đắp các vùng chi tiết phức tạp mà không bị bất kỳ giới hạn nào về lưới hình học.

### Câu hỏi 9: Trong phần thực hành của đồ án, khi nhóm tiến hành huấn luyện LoRA cho Stable Diffusion v1.5 và Action Unit Adapter trên hệ thống GPU A100, thách thức lớn nhất trong việc tinh chỉnh các tham số là gì?
**Trả lời:**  
- Thách thức lớn nhất khi thực nghiệm là tìm kiếm sự cân bằng toán học giữa hai nguồn điều kiện: độ can thiệp của Action Unit và cường độ của Semantic Guidance.
- Nếu trọng số của Action Unit Adapter quá lớn, mạng tạo sinh bị bám quá mức vào các vị trí điểm ảnh cục bộ, khiến ảnh sinh ra bị cứng nhắc, xuất hiện các vệt méo màu xung quanh vùng miệng và mắt. Ngược lại, nếu tăng trọng số Semantic Guidance quá cao, mô hình lại có xu hướng sinh ra các biểu cảm thái quá, làm biến dạng đặc điểm hình thái cá nhân và làm mất đi định danh khuôn mặt gốc. Nhóm đã phải thực hiện thực nghiệm tìm kiếm lưới siêu tham số để tìm ra cấu hình trọng số tối ưu nhất giúp vừa giữ vững định danh cá nhân vừa duy trì độ biểu cảm chuẩn xác.

### Câu hỏi 10: Nhóm đã thực hiện phần mở rộng thực nghiệm trên bộ dữ liệu KDEF nhằm mục đích gì? Khả năng tổng quát hóa của SynFER trên bộ dữ liệu mới này được đánh giá ra sao?
**Trả lời:**  
- Mục đích của phần mở rộng trên bộ dữ liệu KDEF là để kiểm chứng năng lực tổng quát hóa của mô hình tạo sinh trên một phân phối dữ liệu mới hoàn toàn ngoài bài báo gốc. KDEF là bộ dữ liệu khuôn mặt được chụp trong môi trường phòng thí nghiệm tiêu chuẩn với màu da, độ tương phản và góc chiếu sáng rất khác biệt so với tập ảnh thu thập tự nhiên trong AffectNet mà tác giả dùng để huấn luyện.
- Khi đem mô hình SynFER áp dụng lên KDEF mà không cần huấn luyện lại, kết quả đánh giá cho thấy mô hình thích nghi cực kỳ xuất sắc. Hệ thống không bị overfit vào bối cảnh của AffectNet mà vẫn nhận diện và bám sát các Action Unit trên đối tượng mới, sinh ra ảnh biểu cảm chuẩn xác với độ chân thực cao, giữ nguyên vẹn định danh của các tình nguyện viên trong bộ KDEF. Điều này khẳng định tính ổn định vững chắc của kiến trúc SynFER.

### Câu hỏi 11: Theo nhóm, hướng ứng dụng thực tiễn tiềm năng nhất của kiến trúc SynFER trong ngành công nghiệp hiện nay là gì, và cần khắc phục hạn chế kỹ thuật nào để đạt được điều đó?
**Trả lời:**  
- Hướng ứng dụng tiềm năng và giá trị nhất của SynFER là đóng vai trò như một nhà máy sản xuất dữ liệu tổng hợp vô tận và sạch để huấn luyện các hệ thống lái xe tự hành và trợ lý y tế chăm sóc sức khỏe tinh thần. Trong các lĩnh vực này, việc nhận dạng sớm các trạng thái mệt mỏi, căng thẳng hay hoảng loạn của tài xế và bệnh nhân là cực kỳ quan trọng, nhưng dữ liệu thực tế lại rất hiếm và vướng mắc nghiêm trọng về pháp lý quyền riêng tư.
- Để triển khai vào thực tế sản xuất, hạn chế lớn nhất cần khắc phục là tốc độ suy luận chậm của Diffusion model lặp 50 bước. Giải pháp kỹ thuật khả thi nhất là tích hợp các công nghệ chưng cất mô hình mới như Latent Consistency Models (LCM) hoặc SDXL Turbo vào quy trình SynFER, giúp giảm số bước khử nhiễu xuống dưới 5 bước, cho phép sinh dữ liệu tức thì hoặc thậm chí hỗ trợ tạo sinh avatar biểu cảm tương tác theo thời gian thực.
