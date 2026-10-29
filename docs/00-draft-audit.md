# Audit bản draft SmartDesk (01 → 04)

> Phạm vi audit: `01_TOP_DOWN_RESEARCH.md`, `01_xmind_top_down.png`, `02_USE_CASES_INVEST.md`, `02_usecases_employee.png`, `02_usecases_operations.png`, `03_RELUME_INFORMATION_ARCHITECTURE.md`, `03_relume_sitemap_*.png`, `04_UIUX_BLUEPRINT.md`, `SmartDesk_Interactive_Prototype.html`.
> Đối chiếu với format của repo tham khảo [PhamHiep948/finance-manager](https://github.com/PhamHiep948/finance-manager) (README theo bước + `docs/` tách scope, use case, INVEST, IA; mind map XMind; use case có system boundary; INVEST có review từng story).

**Kết luận chung:** nội dung nghiệp vụ của draft **tốt và đúng hướng** (phân biệt Incident / Service Request / Change, AI không tự ghi DB, tenant isolation, state machine riêng). Nhưng **chưa đạt** ở 4 điểm: (1) ảnh mind map không phải XMind và lỗi font; (2) use case diagram thiếu actor/UC; (3) IA chưa phải Relume thật và trộn Việt–Anh; (4) roadmap/scope mâu thuẫn giữa các file, prototype vi phạm chính các rule đã viết. Mức độ: 🔴 phải sửa · 🟠 nên sửa · 🟢 nhỏ.

## 1. Top-down research

| # | Mức | Vấn đề | Đã sửa |
|---|---|---|---|
| 1.1 | 🔴 | `01_xmind_top_down.png` **không phải xuất từ XMind** (render HTML), các mũi tên `→` bị lỗi font thành `□` ở subtitle, footer và nhánh WHEN. | Tạo file `.xmind` thật (2 sheet) + ảnh PNG, toàn bộ tiếng Anh. |
| 1.2 | 🔴 | Mâu thuẫn scope: §1.5 ghi "In scope V1: … 1 change template (ISP Change)" nhưng mind map ghi "Đổi ISP: change phase 2", UC27 = P2 và §2.7 xếp US27 vào Phase 2. | Thống nhất: ISP Change = **Phase 2**. |
| 1.3 | 🔴 | §1.5 ghi "2 request templates (VPN Access, Laptop Provisioning)" nhưng mọi flow/prototype lại dùng **VPN Incident**, không phải VPN Access request. | Template V1: VPN Incident, VPN Access, Laptop Provisioning (+ ISP Change ở Phase 2). |
| 1.4 | 🟠 | Bảng "Đối chiếu thị trường" đưa *HandmadeFinance repository* và *Relume* vào như đối thủ — đó là tài liệu tham khảo phương pháp, không phải bằng chứng thị trường. | Tách thành *Market evidence* và *Method references*. |
| 1.5 | 🟠 | Mind map nhánh MVP ghi "38 use cases toàn phạm vi" — lẫn backlog với MVP. | Nhánh Scope chia MVP / V1 / Phase 2 / Out. |
| 1.6 | 🟠 | Thiếu phân tích **gap / positioning** (vì sao SME cần SmartDesk thay vì Jira SM/Freshservice). | Thêm mục Positioning hypothesis, ghi rõ là giả thuyết. |
| 1.7 | 🟢 | Mind map draft chỉ có 1 góc nhìn; repo tham khảo dùng mind map **chức năng** (module → feature). | Thêm sheet 2 *Feature map* (8 module → 38 UC). |

## 2. Use case diagram & INVEST

| # | Mức | Vấn đề | Đã sửa |
|---|---|---|---|
| 2.1 | 🔴 | Diagram operations **thiếu UC03, UC04, UC05** và **thiếu actor Platform Admin**; Org Admin chỉ có UC23. → 3/38 UC không xuất hiện trên bất kỳ diagram nào. | 3 diagram phủ đủ 38 UC, 6 actor. |
| 2.2 | 🔴 | UC01/UC02 gán actor "User" trong bảng nhưng diagram chỉ nối Employee → IT Staff/Manager/Admin không có đường đăng nhập. | Thêm actor trừu tượng **User** + generalization. |
| 2.3 | 🟠 | Actor phụ *External AI Provider* có trong bảng nhưng không có trên diagram UC12–UC15. | Thêm secondary actor *AI Provider* (bên phải boundary). |
| 2.4 | 🟠 | Nhãn UC tiếng Việt, UC15 bị cắt "…tự…", thứ tự UC lộn xộn (UC20, UC18 nằm sau UC33). | Nhãn tiếng Anh, nhóm theo package, sắp theo số. |
| 2.5 | 🔴 | Roadmap §2.7 sai phụ thuộc: **US29 (cấp laptop) ở MVP-A nhưng US25 (phê duyệt) ở MVP-B**, trong khi AC của US29 yêu cầu request đã Approved. | US25 vào Release 1 (MVP). |
| 2.6 | 🔴 | **US02, US03 không thuộc release nào**; US11/13/15/20/22/30/32 là P1 nhưng bị xếp vào "Phase 2" — trái định nghĩa "P1 = V1 mở rộng". | Release 1 = P0 (21), Release 2 = P1 (14), Phase 2 = P2 (3). |
| 2.7 | 🟠 | Không có cột **Dependencies** và **review INVEST từng story** như repo. | Thêm cả hai. |
| 2.8 | 🟠 | Một số story không *Estimable/Testable*: US10 "trong khoảng thời gian cho phép" (bao lâu?), US37 "ngưỡng cấu hình" (mặc định?), US23 quá lớn. | Định nghĩa mặc định (reopen 7 ngày, cảnh báo 80% / 100%), US23 ghi rõ cách tách task. |
| 2.9 | 🟢 | AC chỉ có cho 9/38 UC. | Mỗi story có ≥1 AC chính + 1 AC phủ định; giữ G/W/T chi tiết cho 9 UC quan trọng. |

## 3. Information architecture (Relume)

| # | Mức | Vấn đề | Đã sửa |
|---|---|---|---|
| 3.1 | 🔴 | Ảnh Relume **trộn Việt–Anh** ("Khung hội thoại", "tìm KB", "nút vẫn cần hỗ trợ □ tạo ticket" – lỗi font). Yêu cầu: tiếng Anh. | Viết lại toàn bộ tiếng Anh. |
| 3.2 | 🔴 | Chưa đúng kiểu Relume: mỗi section chỉ là 1 nhãn 1–3 chữ, **không mô tả chức năng**; mũi tên giữa các card vô nghĩa (SCR-02 → SCR-05?). `03_relume_sitemap_full.png` chỉ là cây nhóm, không có section. | Mỗi page card = danh sách section, mỗi section có **tên + mô tả chức năng**, sitemap dạng cây như Relume. |
| 3.3 | 🔴 | **Thiếu màn**: không có Profile (UC02), Notification center (UC37), 403/404, Change review (UC27), Approval rules (UC24). | Bổ sung → 30 màn. |
| 3.4 | 🟠 | Không có bảng **Requirement → Screen** (repo có). Không kiểm được mọi UC có entry point. | Thêm traceability UC → SCR, 38/38 có màn. |
| 3.5 | 🟠 | Asset Inventory chỉ cho IT Staff nhưng UC32 là của IT Manager. | Cho Manager quyền đọc SCR Inventory/Asset detail. |
| 3.6 | 🟢 | Câu "không sao chép cấu trúc menu trong README tham khảo" không có ý nghĩa với người đọc. | Bỏ. |

## 4. UI/UX blueprint & prototype

| # | Mức | Vấn đề | Đã sửa |
|---|---|---|---|
| 4.1 | 🔴 | Blueprint tham chiếu `04_wireframe_*.png` **nhưng các file này không tồn tại**. | Chụp màn prototype thật vào `docs/images/ui/`. |
| 4.2 | 🔴 | Prototype **vi phạm rule AI**: mọi câu hỏi không khớp regex đều trả lời bài VPN KB-024 kèm "nguồn" → chính là "bịa nguồn" mà UC12 cấm. | Thêm nhánh *insufficient evidence* → không cite, đề nghị tạo ticket / mở catalog. |
| 4.3 | 🔴 | Agent bấm **Resolved không cần resolution note** (trái US21); Manager **Reject không cần lý do** (trái US25). | Validate bắt buộc trong prototype. |
| 4.4 | 🟠 | Tạo SR-2026-0105 xong lại mở chi tiết **IT-1042 VPN** → luồng demo sai. Status "Hoàn tất" không có trong state machine. Priority IT-1042 là Normal (employee) nhưng High (agent). | Detail theo ID; dùng đúng state names; dữ liệu nhất quán. |
| 4.5 | 🟠 | "Ticket Detail" là item trên sidebar — trái nguyên tắc list → detail của IA. Manager có "Ticket Queue" nhưng không có Inventory (UC32). | Sidebar theo IA mới. |
| 4.6 | 🟠 | Screen transition bước 7 "Approval → Fulfillment" là chuyển **giữa 2 actor** nhưng ghi như cùng một user. | Ghi rõ handoff qua notification. |
| 4.7 | 🟢 | Prototype tiếng Việt trong khi tài liệu/ảnh yêu cầu tiếng Anh. | Prototype tiếng Anh. |

## Những gì giữ nguyên từ draft

- Định nghĩa Incident / Service Request / Change và 3 state machine riêng.
- Nguyên tắc AI: chỉ đọc KB đã publish + có quyền, không tự submit, không phê duyệt, idempotency key.
- 3 kịch bản S1 VPN / S2 Laptop / S3 ISP, KPI giả thuyết (ghi rõ chưa có số liệu thật).
- Bộ AC Given/When/Then cho UC07, 12, 14, 15, 19, 25, 29, 34, 37.
