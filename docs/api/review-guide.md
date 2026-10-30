# SmartDesk OpenAPI 3.1 v0.2 — Review guide for Claude

**Ngày đối chiếu:** 2026-10-30  
**Hợp đồng cần review:** `smartdesk-openapi-reviewed-v2.yaml` (đặt vào repo dưới `docs/api/openapi.yaml`)  
**Nguồn sản phẩm:** https://github.com/cuonglpv/SmartDesk  
**Trạng thái:** PROPOSED / DESIGN ONLY — repository hiện chỉ có tài liệu, diagram, `tools/model.py` và một UX prototype dùng mock data; **chưa có backend/API đang chạy**.

## 1. Nguồn để review theo thứ tự

1. `docs/02-use-cases.md` — 43 UC, vai trò, quyền, trạng thái ticket.
2. `docs/06-acceptance-criteria.md` — điều kiện nghiệm thu, HTTP code và tình huống phủ định.
3. `docs/03-invest-requirements.md` — priority, dependency, INVEST, release.
4. `docs/01-top-down-research.md` — business intent, SLA, asset/AI constraints.
5. `docs/04-information-architecture.md` — mapping tới màn hình và chức năng.
6. `docs/05-ui-ux.md` và `prototype/index.html` — kiểm tra các journey, không coi mock API là backend.
7. `tools/model.py` — nguồn dữ liệu sinh sơ đồ.

## 2. Phạm vi hợp đồng đề xuất

| Hạng mục | Kết quả |
|---|---:|
| OpenAPI | 3.1.0 |
| API operations | 99 |
| Unique API paths | 85 |
| Reusable schemas | 134 |
| Use case được trace | 43/43 |
| Operations đánh dấu P0 | 49 |
| Operations đánh dấu P1 | 43 |
| Operations đánh dấu P2 | 7 |

**Bản 0.3.0-draft** (sau khi áp [openapi-review.md](openapi-review.md)): 105 operations, 91 paths, 135 schemas; P0 53 / P1 45 / P2 7; vẫn 43/43 UC. **Bản 0.4.0-draft** chốt D15 (refresh token chỉ qua HttpOnly cookie): 105 operations, 91 paths, 134 schemas. Bảng trên giữ số liệu của 0.2 để đối chiếu.

**Lưu ý:** số operations không bằng số use cases vì một UC có thể cần nhiều endpoint và một endpoint có thể phục vụ nhiều UC. Giá trị `x-implementation-status: PROPOSED` không có nghĩa đã được implement. `x-release` trên operation đa UC biểu thị mốc mở API sớm nhất; các feature triển khai sau phải được feature-gate theo UC.

## 3. Các quyết định thiết kế đang tạm chọn

- **Tenant isolation:** tenant lấy từ authenticated principal/session, không có `X-Tenant-Id` từ client. Mọi truy vấn và file/embedding phải lọc tenant + quyền của principal trước khi trả dữ liệu. `PLATFORM_ADMIN` chỉ có access metadata tenant, không được xem tickets/attachments của khách hàng.
- **RBAC + ownership:** permissions nằm ở `x-permissions` với nghĩa ANY-OF trên capability entry; policy cụ thể theo resource, ownership, permission phụ và state vẫn bắt buộc. Role grants kế thừa quyền self-service theo bảng use case.
- **Auth:** dùng short-lived bearer access token kèm server-side revocation; thiết kế cookie HttpOnly + CSRF hoặc OAuth/OIDC vẫn là lựa chọn thay thế cần quyết định.
- **Multi-workspace login:** chỉ hiển thị lựa chọn tenant sau khi password đã xác thực; challenge một lần, sống ngắn.
- **Optimistic locking:** các command có `expectedVersion` và trả `409 CONCURRENT_MODIFICATION` nếu stale, khớp AC; không dùng `If-Match`/`412` trong bản này.
- **Ticket idempotency:** `POST /tickets` bắt buộc `Idempotency-Key`; scope = tenant + actor + method + path; phải lưu hash payload và response tối thiểu 24 giờ.
- **Approval:** hành động phê duyệt vẫn là của người có quyền, `REJECT` bắt buộc reason; một tài sản chỉ có một assignment active; handover phải atomically update ticket + asset + audit.
- **AI:** không có endpoint cho LLM trực tiếp POST ticket. Backend trả ticket draft, con người duyệt và thực hiện `POST /tickets`; citations chỉ từ KB published + user-visible; `NO_SOURCE` không bịa citations.
- **KB + asset:** KB drafts không được search/index; sau retire deny read và retrieval ngay cả khi vector index chưa sync. Asset status không được update thẳng thành ASSIGNED mà phải có handover.
- **SLA:** business calendar và timezone thuộc tenant; pause `WAITING_FOR_EMPLOYEE`; cảnh báo warning default 80%, breach 100%, alert generation phải idempotent.
- **P0 tenant bootstrap:** tạm thiết kế seed default IT Support routing team và 3 catalog templates (VPN Incident, VPN Access, Laptop Provisioning). Đây là giả định kỹ thuật, chưa phải requirement đã chốt.

## 4. Các mâu thuẫn/điểm cần Claude phản biện nghiêm túc

| # | Nơi cần đối chiếu | Vấn đề / quyết định tạm |
|---|---|---|
| D01 | AC-UC01 vs AC-UC41 / UC01 | AC-UC01 nói suspended tenant login trả `401` generic; AC-UC41 lại cho phép đăng nhập read-only. **Bản API chọn chặn login** để fail-closed; cần product owner quyết định. |
| D02 | `01-top-down-research.md` §1.7 vs `02-use-cases.md` | Bảng scope 01 có `21 P0 / 14 P1 / 3 P2` nhưng catalog UC ghi `22 P0 / 18 P1 / 3 P2` = 43. **Dùng catalog UC làm nguồn trace**, không dùng số liệu scope sai. |
| D03 | UC10 + ticket state diagrams | AC-UC10 cho reopen mọi ticket RESOLVED, nhưng state machine SERVICE_REQUEST không có REOPENED. Cần xác nhận bổ sung transition hay giới hạn reopen chỉ Incident. |
| D04 | UC24 + vai trò | Rule có thể chỉ định approver role/person; bảng phân quyền chỉ `IT_MANAGER` có quyền approve. Bản API giới hạn cho IT_MANAGER; delegated approval cần mô hình quyền rõ ràng. |
| D05 | UC23 / catalog | Dynamic fields của request type không thể mô tả đầy đủ bằng OpenAPI schema tĩnh. API dùng `answers: map<string, JsonValue>`; backend phải validate bằng **snapshot published form version**, reject unknown fields/stale version. |
| D06 | UC17 + UC36 | Đổi priority “restarts SLA targets”, trong khi SLA policy snapshot khi create. Cần chốt tính lại due-date thế nào, giữ elapsed time thế nào, audit thế nào. |
| D07 | UC26 + UC29 | Fulfilment checklist “all done resolves” và asset handover cũng “resolves”; cần tránh double resolve/race và đảm bảo complete checklist đúng nghiệp vụ. |
| D08 | UC27 + change diagram | CHANGE `PENDING_APPROVAL -> SCHEDULED` nhưng có chức năng reschedule; cần định nghĩa chính xác schedule window, approval condition, rollback, close operation. |
| D09 | UC03 + UC23 | `routingTeamId` xuất hiện trong catalog nhưng docs chưa định nghĩa API tạo/team membership rõ; bản đề xuất bổ sung `/organization/teams`. Cần confirm ownership. |
| D10 | UC33/34 | Trạng thái KB DRAFT/IN_REVIEW/PUBLISHED/RETIRED, luồng sửa bài đã publish, replacement version và lỗi async reindex chưa mô tả đủ; cần chốt publish invariant. |
| D11 | UC11 + UC32 | Employee chỉ nên đọc `MyAssignedAsset` (tag, model, handover); IT xem đầy đủ serial/stock. Cần kiểm tra no overfetch/no PII leak. |
| D12 | UC07/UC09 | Giới hạn file 10 MiB và allow-list được ghi, nhưng malware scanning, content-sniffing, upload expiry, download authorization là đề xuất kỹ thuật nên cần confirm. |
| D13 | UC01, UC04 | User/Member/Tenant identity khi cùng email thuộc nhiều tenant, invitation conflict và reset/session revocation cần mô tả phân biệt global identity và tenant membership. |
| D14 | Release 1 vs Release 2 | Một số response có trường SLA/P1 hoặc hỗ trợ feature P1 dùng chung route P0. Phải feature-gate chức năng P1, không hứa P1 chạy ở MVP. |
| D15 | OAS 3.1 + bearer | **Đã chốt (0.4.0-draft):** access token bearer giữ trong memory; refresh token chỉ trong cookie HttpOnly `sd_refresh` (SameSite=Strict, Path=/v1/auth), xoay vòng mỗi lần refresh, CSRF double-submit `X-CSRF-Token`. Còn mở: định dạng và thời hạn access token. |
| D16 | Scope | Media upload cho ảnh KB editor, search index lifecycle, async jobs/notification delivery và team routing cần API/async-event contract riêng nếu đi vào triển khai. |

## 5. Bắt buộc review bằng test cases

| Test | Tình huống | Kết quả cần bảo đảm |
|---|---|---|
| T01 | Employee của tenant A gọi `/tickets/{id}` với ID của tenant B | `404`, không leak ID, title hoặc các nội dung khác |
| T02 | Platform Admin truy cập ticket, attachment hoặc KB nội bộ tenant | `403`, kể cả tự đoán URL |
| T03 | Employee lấy internal comment/attachment qua timeline hoặc direct file endpoint | Không lộ content/metadata, trả `404` hoặc lọc theo policy |
| T04 | Cùng `Idempotency-Key` + cùng body gọi tạo ticket 2 lần | Chỉ tạo 1 ticket, replay original response |
| T05 | Cùng key + body khác | `409 IDEMPOTENCY_KEY_REUSED` |
| T06 | Hai IT Staff pick up ticket với cùng `expectedVersion` | Một thành công; một `409` |
| T07 | Hai IT Staff handover cùng asset | Một thành công; một `409`, không tạo 2 active assignments |
| T08 | Laptop request chưa approved nhưng gọi handover/fulfilment | `409 APPROVAL_REQUIRED` |
| T09 | IT Staff gọi approve | `403` |
| T10 | Reject không reason | `400` hoặc field validation error; không đổi trạng thái |
| T11 | IT set CLOSED trực tiếp hoặc resolve thiếu note | `409` (invalid transition) hoặc `400` (missing note) |
| T12 | Requester reopen sau deadline 7 ngày | `409` |
| T13 | Auto-close job chạy lại | Chỉ một close event; không ghi duplicate |
| T14 | Bài KB chưa published, bài của tenant B, bài đã retired đi qua AI | Không được trích dẫn / retrieval; trả NO_SOURCE |
| T15 | Assistant đưa draft nhưng chưa có POST /tickets của người dùng | Database không có ticket mới |
| T16 | Employee gửi `requesterId`, `tenantId`, `role` trái phép trong body | `400` và không override server principal |
| T17 | Dùng request-type version cũ/ẩn | `409 CATALOG_VERSION_STALE` hoặc `404` cho người không được phép |
| T18 | Two simultaneous approval decisions on one record | Một thành công, một `409`, audit đúng một quyết định |
| T19 | Org Admin thử lock/demote Org Admin active cuối cùng | `409`, không mất quyền quản trị tổ chức |
| T20 | File từ internal note được tải qua guessed attachment id | `404`, không lộ metadata/file |
| T21 | Thiết bị trạng thái RETIRED nhận maintenance | `409` |
| T22 | IT Manager gọi write asset | `403` theo role matrix |
| T23 | Bộ lọc báo cáo/CSV/PDF trùng nhau | Cùng tập dữ liệu và tổng số; PII được kiểm soát |
| T24 | Cảnh báo SLA chạy lại ở ngưỡng 80%/100% | Không gửi alert trùng |


## Bổ sung sau khi tham khảo finance-manager

**Repo tham khảo:** https://github.com/PhamHiep948/finance-manager (tập trung `docs/api/openapi.yaml` và `docs/api/README.md`). Chỉ học cách đóng gói tài liệu, không lấy mô hình tài chính hoặc single-tenant làm ràng buộc SmartDesk.

Điểm mới của bản `0.2.0-draft`:

- Giữ **OpenAPI 3.1**; không cần hạ sang 3.0.4 của finance-manager.
- Chuẩn hóa toàn bộ error responses thành `application/problem+json`, dùng **RFC 9457 ProblemDetails**, thêm `errorCode`, `traceId`, `errors`. `ErrorResponse` cũ chỉ giữ deprecated để đối chiếu. **Đây là thay đổi BREAKING so với contract 0.1** (chưa có backend nên không ảnh hưởng runtime).
- Thêm `x-roles` (gợi ý vai trò), `x-data-scope` (mô tả phạm vi), và giữ `x-permissions` là capability gate. Role metadata KHÔNG được thay thế kiểm tra quyền trên resource.
- Bổ sung ví dụ tạo ticket, 201 ticket response, paginated empty list, AI no-source, approval, handover và lỗi.
- Tạo `smartdesk-api-readme-v2.md` hướng dẫn header, MIME, ví dụ cURL, auth, role, pagination, tenant và luồng thực tế.
- Tạo `smartdesk-api-traceability-v2.md` liệt kê đầy đủ UC01–UC43 theo API và operationId.
- Thêm `500` reusable Problem Details vào 99 operations; `429` vẫn chỉ có trên các operation được đánh dấu trong draft (cần policy rate-limit chính thức).

**Review mở rộng so với contract 0.1:**

1. Kiểm tra 5 `x-roles` mapping có mâu thuẫn với `x-permissions` hoặc UC role table không; đặc biệt triage, change management, catalog editor, approval decision.
2. Xác nhận 403/404 có nhất quán với scoping & IDOR (Platform Admin 403, cross-tenant resource ID 404).
3. Kiểm tra error payload của **mọi 4xx/5xx** đúng RFC 9457 và status, không lộ nội bộ qua `detail`, `errors` hoặc `traceId`.
4. Kiểm tra 8 representative JSON examples thực sự conform to schema; kiểm tra các ví dụ cũ còn lại.
5. Chốt lỗi upload quá 10 MB: `AC-UC07` muốn `400`, contract đề xuất `413`. Hãy phân loại là SOURCE/CONTRACT mismatch và đề xuất quyết định rõ ràng.
6. Cân nhắc whether `429` rate limit được mô tả đồng đều ở mọi endpoint; không tự thêm rate-limit behavior khi chưa thống nhất.
7. Review toàn bộ 43 UC matrix; đánh giá `mapped` vs `fully specified` riêng, tránh tính mapping là compliance.
8. Chưa xác minh Redocly/Spectral OpenAPI-specific syntax; yêu cầu chạy `npx @redocly/cli lint` và `bundle`, không khẳng định production-ready.

**Đã chạy kiểm tra local cho v0.2:** PyYAML, duplicate YAML key, unique operation IDs, `$ref`, path params, `jsonschema.Draft202012Validator.check_schema`, và **498 lần validate examples (bao gồm error examples được dùng lặp lại)**: 0 lỗi. Đây không phải OAS metaschema lint chính thức hoặc kiểm tra API runtime.

## 6. Prompt review nghiêm ngặt dành cho Claude

> Hãy đóng vai Principal Backend Architect, Security Reviewer và OpenAPI Specification Reviewer. Đọc **toàn bộ** `smartdesk-openapi-reviewed-v2.yaml` và đối chiếu trực tiếp với repo `https://github.com/cuonglpv/SmartDesk`, đặc biệt `docs/02-use-cases.md` và `docs/06-acceptance-criteria.md`. Đây là **proposed contract**, repository chưa có backend. Không được mặc định endpoint đã implement.
>
> Yêu cầu review: (1) OAS 3.1 formal validity: parameters, `$ref`, schema, response codes, security, examples; (2) coverage 43/43 UC và correctness P0/P1/P2; (3) role+permission+tenant+ownership matrix, IDOR, privilege escalation và data leakage; (4) Incident/Service Request/Change state machine và illegal transitions; (5) concurrency/idempotency/transaction boundaries cho ticket, approval, asset handover; (6) dynamic catalog form validation/versioning; (7) AI grounding, citation integrity, KB visibility và AI không tự write; (8) file upload/download security; (9) SLA calendar, pause, thresholds, exports; (10) UX API completeness cho toàn bộ 30 screens.
>
> **Báo cáo bắt buộc:** Mỗi phát hiện có severity `BLOCKER/HIGH/MEDIUM/LOW`, đường dẫn endpoint/schema, quy tắc gốc trong repo, cách tái hiện/tấn công, phương án sửa cụ thể và ví dụ YAML được sửa. Tách rõ **source contradiction**, **contract defect** và **product decision not yet specified**. Không nhận xét chung chung. Ưu tiên lỗi phá tenant isolation, cho AI tự submit, sai approval/handover, hoặc lộ internal notes. Kết thúc bằng bảng 43 UC với PASS/PARTIAL/MISSING và danh sách 10 việc phải sửa trước khi implement MVP.

## 7. Kiểm tra đã thực hiện trên artifact

- Parse YAML thành công (PyYAML).
- Không có operationId trùng.
- 43/43 UC có ít nhất một operation ghi `x-use-cases`.
- Toàn bộ `$ref` nội bộ đều trỏ đến schema/parameter/response có thật.
- Tất cả path parameter `{...}` đều được khai báo và đánh dấu `required`.
- 134 schemas vượt qua `jsonschema.Draft202012Validator.check_schema` (kiểm tra cú pháp JSON Schema 2020-12).

**Chưa thực hiện:** official OAS metaschema lint (Spectral/Redocly/Swagger Editor), contract test với backend, security pen-test, performance benchmark. Không nên coi việc parse YAML là xác nhận spec production-ready.


## 8. Prompt bổ sung bắt buộc sau khi tham khảo finance-manager

> Review đồng thời `docs/api/openapi.yaml`, `docs/api/README.md`, `docs/api/traceability.md`. Tham khảo `https://github.com/PhamHiep948/finance-manager/tree/main/docs/api` chỉ về cấu trúc tài liệu, standardized Problem Details, x-roles và examples, KHÔNG sao chép finance API. Bắt lỗi từng contract mismatch với SmartDesk `UCxx/AC-UCxx`; nêu HTTP status, request/response, data isolation và bản vá YAML. Trích cụ thể tại sao `x-roles` chỉ là coarse metadata và dùng `x-permissions`/ownership/state để kiểm tra enforcement. Phân loại BLOCKER/HIGH/MEDIUM/LOW và chỉ đưa ra danh sách PASS khi có bằng chứng; nếu chưa chắc, đánh dấu OPEN DECISION.
