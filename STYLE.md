# Hướng dẫn Trình bày Báo cáo LaTeX (Report Formatting & Style Guidelines)

Tài liệu này tổng hợp toàn bộ các quy tắc trình bày và định dạng tài liệu LaTeX đã được thống nhất. Hãy tuân thủ nghiêm ngặt các hướng dẫn này khi soạn thảo các chương và bài viết trong báo cáo.

---

## 1. Không Sử dụng Thuật ngữ Tiếng Anh đi kèm Phụ chú (No English Subtitles)

* **Quy tắc:** Không đặt thuật ngữ tiếng Anh trong dấu ngoặc đơn ngay sau thuật ngữ tiếng Việt ở các tiêu đề mục hoặc trong nội dung văn bản. Chỉ sử dụng thuật ngữ tiếng Việt chuẩn hóa hoặc sử dụng trực tiếp thuật ngữ tiếng Anh nếu không có từ dịch nghĩa tương đương phù hợp.
* **Ví dụ:**
  * **Sai:** `Cây quyết định (Decision Tree)` hoặc `Thuật toán Naive Bayes (Naive Bayes Algorithm)`.
  * **Đúng:** `Cây quyết định` hoặc `Thuật toán Naive Bayes`.

---

## 2. Trình bày Dạng Đoạn văn thay vì Liệt kê (Prose over Lists)

* **Quy tắc:** Khi giải thích các bước thực hiện, mô tả đặc điểm hoặc vai trò của các thành phần, hạn chế tối đa việc sử dụng danh sách liệt kê dạng gạch đầu dòng (`itemize` hoặc `enumerate` với cấu trúc lặp đi lặp lại như `\item \textbf{Mô tả:}` và `\item \textbf{Vai trò:}`). Hãy chuyển đổi các ý này thành các đoạn văn xuôi (prose) liền mạch, diễn đạt tự nhiên và học thuật.
* **Ví dụ:**
  * **Sai:**
    ```latex
    \begin{itemize}
        \item \textbf{Mô tả:} Cây quyết định là một mô hình phân lớp...
        \item \textbf{Vai trò:} Giúp trực quan hóa quá trình ra quyết định...
    \end{itemize}
    ```
  * **Đúng:**
    "Cây quyết định là một mô hình phân lớp cấu trúc dạng cây, trong đó mỗi nút trong đại diện cho một thuộc tính. Mô hình này đóng vai trò quan trọng trong việc trực quan hóa quá trình ra quyết định và trích xuất luật phân lớp một cách rõ ràng."

---

## 3. Chú thích của Bảng biểu (Table Captions)

* **Quy tắc:** Chú thích (caption) của bảng biểu phải luôn được đặt ở **phía trên** của bảng đó.
* **Ví dụ:**
    ```latex
    \begin{table}[htbp]
    \caption{Bảng phân phối xác suất của các thuộc tính.}
    \label{tab:probability_distribution}
    \centering
    \begin{tabular}{ccc}
    ...
    \end{tabular}
    \end{table}
    ```

---

## 4. Không Kẻ đường dọc trong Bảng (No Vertical Table Borders)

* **Quy tắc:** Tuyệt đối không sử dụng đường kẻ dọc (`|`) để ngăn cách các cột trong môi trường bảng biểu (`tabular`, `tabularx`, v.v.). Chỉ sử dụng đường kẻ ngang (`\hline` hoặc tốt nhất là các lệnh kẻ ngang chuyên dụng từ gói `booktabs` như `\toprule`, `\midrule`, `\bottomrule`) để phân chia tiêu đề và dữ liệu.
* **Ví dụ:**
* **Sai:** `\begin{tabular}{|c|c|c|}`
* **Đúng:**
```latex
\begin{tabular}{ccc}
\toprule
Thuộc tính & Giá trị & Xác suất \\
\midrule
A & Lớn & 0.6 \\
B & Nhỏ & 0.4 \\
\bottomrule
\end{tabular}

```





---

## 5. Chú thích của Hình ảnh và Sơ đồ (Figure Captions)

* **Quy tắc:** Chú thích (caption) của hình ảnh hoặc sơ đồ phải luôn được đặt ở **phía dưới** của hình vẽ/sơ đồ đó.
* **Ví dụ:**
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{decision_tree_diagram.png}
\caption{Sơ đồ cấu trúc cây quyết định sau khi huấn luyện.}
\label{fig:decision_tree}
\end{figure}

```



---

## 6. Đánh số Toàn bộ Công thức Toán học (Numbered Equations)

* **Quy tắc:** Tất cả các công thức toán học hiển thị độc lập (display math) bắt buộc phải được đánh số thứ tự. Tránh sử dụng định dạng không đánh số như cặp ký tự song song `$$ ... $$` hoặc môi trường `align*`. Hãy thay thế bằng các môi trường toán học chuẩn có đánh số như `equation` hoặc `align`.
* **Ví dụ:**
* **Sai:** `$$ P(A|B) = \frac{P(B|A)P(A)}{P(B)} $$`
* **Đúng:**
```latex
\begin{equation}
P(A|B) = \frac{P(B|A)P(A)}{P(B)}
\end{equation}

```





---

## 7. Dấu câu sau Công thức Toán học (Equation Punctuation)

* **Quy tắc:** Công thức toán học hiển thị độc lập là một phần ngữ pháp của câu, vì vậy bắt buộc phải có dấu câu ở cuối công thức:
* Sử dụng **dấu phẩy (`,`)** ở cuối công thức nếu ngay sau công thức là đoạn giải thích ý nghĩa các ký hiệu (ví dụ: ", trong đó...", ", với...").
* Sử dụng **dấu chấm (`.`)** ở cuối công thức nếu công thức đó kết thúc câu hoàn chỉnh và đoạn văn tiếp theo bắt đầu một câu mới hoặc đoạn mới.


* **Ví dụ:**
* **Trường hợp dùng dấu phẩy (Giải thích ký hiệu):**
```latex
\begin{equation}
Gain(S, A) = Entropy(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} Entropy(S_v),
\end{equation}
trong đó $S_v$ là tập con của $S$ chứa các phần tử có thuộc tính $A$ nhận giá trị $v$.

```


* **Trường hợp dùng dấu chấm (Kết thúc câu):**
```latex
\begin{equation}
E = mc^2.
\end{equation}
Hệ thức trên biểu thị mối liên hệ tương đương giữa khối lượng và năng lượng.

```





---

## 8. Không Sử dụng Cụm từ In đậm Tóm tắt ở Đầu Mục Liệt kê (No Bold Introductory Phrases in Lists)

* **Quy tắc:** Khi bắt buộc phải sử dụng danh sách liệt kê, không chèn thêm các cụm từ in đậm mang tính chất tóm tắt ý hoặc đặt nhãn từ khóa (`\textbf{...}:`) ở ngay đầu mỗi mục dữ liệu (`\item`). Lối trình bày này làm vụn văn bản và giảm tính chuyên nghiệp của văn phong khoa học. Hãy diễn đạt nội dung một cách tự nhiên và trực tiếp ngay từ đầu câu.
* **Ví dụ:**
* **Sai:**
```latex
\begin{itemize}
    \item \textbf{Lãng phí dữ liệu:} Đối với các bài toán có kích thước dữ liệu hạn chế, việc tách một phần dữ liệu làm tập validation chỉ để phục vụ cắt tỉa sẽ làm giảm lượng dữ liệu huấn luyện...
    \item \textbf{Nhạy cảm với cách phân chia:} Quyết định cắt tỉa phụ thuộc rất lớn vào phân phối của tập validation riêng biệt đó...
\end{itemize}

```


* **Đúng:**
```latex
\begin{itemize}
    \item Đối với các bài toán có kích thước dữ liệu hạn chế, việc tách một phần dữ liệu làm tập validation chỉ để phục vụ cắt tỉa sẽ làm giảm lượng dữ liệu huấn luyện, khiến cây quyết định ban đầu được xây dựng trên một tập mẫu không đầy đủ, dẫn đến chất lượng cây bị giảm sút.
    \item Quyết định cắt tỉa phụ thuộc rất lớn vào phân phối của tập validation riêng biệt đó. Nếu tập validation này không mang tính đại diện tốt cho toàn bộ tổng thể, việc cắt tỉa có thể bị quá tay (làm mất thông tin quan trọng) hoặc cắt tỉa thiếu (vẫn giữ lại các nhánh overfitting).
\end{itemize}

```





---

---

# Hướng dẫn Trình bày Slide LaTeX (Slide Formatting & Style Guidelines)

Khi soạn thảo slide báo cáo (sử dụng Beamer hoặc các gói tương đương), cần tuân thủ các tiêu chuẩn thiết kế trực quan và phân phối thông tin để đảm bảo hiệu quả thuyết trình cao nhất.

---

## 9. Hạn chế Tối đa Số lượng Chữ trên Slide (Text Minimization)

* **Quy tắc:** Slide không phải là nơi sao chép nguyên văn nội dung từ báo cáo. Tránh việc đưa vào các đoạn văn dài phức tạp. Hãy cô đọng thông tin thành các từ khóa, đoản ngữ ngắn gọn hoặc sơ đồ hình ảnh. Mỗi slide (frame) chỉ nên truyền tải từ 1 đến 2 ý cốt lõi.
* **Ví dụ:**
* **Sai:** Bê nguyên một đoạn văn dài 5-6 dòng chứa đầy đủ định nghĩa và phân tích vào slide khiến người nghe bị phân tâm do phải đọc chữ.
* **Đúng:** Sử dụng các gạch đầu dòng ngắn gọn diễn đạt từ khóa chính kết hợp với diễn giảng trực tiếp bằng lời nói.



---

## 10. Chú thích và Trích dẫn Nguồn Hình ảnh (Figure Captions & Image Sources)

* **Quy tắc:** Tất cả các hình ảnh, đồ thị hoặc sơ đồ đưa lên slide bắt buộc phải có chú thích (caption) rõ ràng nằm ở **phía dưới** tương tự như trong báo cáo. Nếu hình ảnh được thu thập hoặc kế thừa từ một nghiên cứu khác, phải chèn ký hiệu trích dẫn nguồn ngay cạnh hoặc trong phần chú thích.
* **Ví dụ:**
```latex
\begin{figure}
\centering
\includegraphics[width=0.7\linewidth]{cnn_architecture.png}
\caption{Kiến trúc mạng CNN cải tiến \cite{LeCun2015}.}
\end{figure}

```



---

## 11. Trích dẫn Nguồn trực tiếp trên Slide (In-slide Citations)

* **Quy tắc:** Khi trình bày về các thuật toán, mô hình, hoặc số liệu được lấy từ các công trình khoa học của tác giả khác, bắt buộc phải sử dụng lệnh trích dẫn (`\cite{...}`) ngay tại slide đó. Việc này giúp hội đồng và người nghe dễ dàng theo dõi, đối chiếu độ tin cậy của thông tin mà không cần đợi tới slide cuối cùng.
* **Ví dụ:**
"Thuật toán tối ưu hóa Adam \cite{Kingma2014} được lựa chọn nhờ tốc độ hội tụ nhanh và khả năng thích ứng tốt với tốc độ học."

---

## 12. Danh mục Tài liệu Tham khảo ở Cuối Slide (References Slide)

* **Quy tắc:** Bài thuyết trình phải có tối thiểu một slide cuối cùng dành riêng cho mục "Tài liệu tham khảo" (References). Slide này chỉ liệt kê các nguồn tài liệu thực sự được trích dẫn xuất hiện ở các slide trước đó, sử dụng môi trường chuẩn hóa (`\printbibliography` hoặc `thebibliography`) với định dạng font chữ nhỏ gọn (như `\small` hoặc `\footnotesize`) để tối ưu không gian hiển thị.
* **Ví dụ:**
```latex
\cleardoublepage
\phantomsection
\showsectionframefalse
\section{Tài liệu tham khảo}
\begin{frame}[allowframebreaks]{Tài liệu tham khảo}
    \bibliographystyle{unsrt}
    \bibliography{ref/ref}
\end{frame}

```
