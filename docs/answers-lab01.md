# Lab 01 – Trả lời câu hỏi thảo luận

Sinh viên: Lê Thu Ngân – MSSV 202417257

## Câu hỏi nhanh: cấu hình `--global` được lưu ở đâu? Khác gì so với `--local`?

- `--global` lưu trong tệp `~/.gitconfig` của người dùng hiện tại
  (trên máy em: `C:/Users/Admin/.gitconfig`, xem bằng
  `git config --list --show-origin`). Cấu hình này áp dụng cho **mọi repo**
  của người dùng đó trên máy.
- `--local` (mặc định khi không ghi gì) lưu trong `.git/config` của **một
  repo cụ thể** và chỉ có hiệu lực trong repo đó.
- Thứ tự ưu tiên: `--system` < `--global` < `--local`. Giá trị cụ thể hơn sẽ
  ghi đè giá trị chung, ví dụ có thể dùng email khác cho riêng một repo.

## 1. Vì sao dùng `git mv`?

- `git mv a b` vừa đổi tên tệp trên đĩa vừa cập nhật staging area trong
  một bước (tương đương `mv` + `git rm a` + `git add b`), nên không bị sót
  tệp cũ hay quên add tệp mới.
- Nội dung tệp không đổi, nên Git nhận ra đây là phép **đổi tên** (rename
  100%): `git status` hiện `renamed`, tab *Files changed* của PR #1 hiện
  *renamed* chứ không phải xóa + thêm, người review dễ thấy rằng commit
  chỉ di chuyển tệp.
- Lịch sử tệp được giữ: `git log --follow -- aims/cart.py` vẫn thấy commit
  gốc `feat: add initial DVD, Cart and demo program`, và `git blame` vẫn
  truy được tác giả từng dòng. Trong SCM, đây là việc giữ định danh của
  Configuration Item qua các lần thay đổi.
- Vì vậy tách riêng commit "di chuyển" (`refactor: move sources into aims
  package`) và commit "sửa nội dung" (`refactor: update imports in
  main.py`), để Git không nhầm rename thành xóa + thêm khi nội dung đổi
  nhiều.

## 2. `release/lab01` có phải baseline không?

Có. Baseline là một cấu hình đã được thống nhất, dùng làm mốc và chỉ được
thay đổi qua quy trình kiểm soát. `release/lab01`:

- được tạo từ `master` sau khi PR #1 đã được duyệt và merge, tức là một
  trạng thái đã qua kiểm soát thay đổi;
- là bản nộp bài (bản giao cho "khách hàng" là giảng viên), được định
  danh rõ ràng: `git rev-parse origin/master origin/release/lab01` cho cùng
  mã băm `ae47ae3`;
- không phát triển tiếp trên nhánh này; nếu phải sửa bài đã nộp thì đi qua
  `hotfix/*` + PR (Lab 05).

Lưu ý: nhánh là con trỏ có thể di chuyển, nên baseline chỉ được cố định
tuyệt đối khi gắn thêm **tag** (từ Lab 04, `release/lab01` sẽ được gắn
`v0.1.0`). Tag định danh chính xác phiên bản; nhánh release là dòng bảo
trì của bản phát hành đó.

## 3. Vì sao không commit thẳng lên `master` dù làm một mình?

- **Kiểm soát thay đổi**: mọi thay đổi đều có một Change Request (PR) ghi
  rõ mục đích, nội dung, cách kiểm thử; lịch sử có merge commit
  `Merge pull request #1` để truy vết *ai, khi nào, vì sao*.
- **`master` luôn ở trạng thái chạy được**: làm trên nhánh riêng, kiểm tra
  (`python main.py` → 63.89 $) xong mới tích hợp. Nếu hỏng thì bỏ nhánh,
  `master` không bị ảnh hưởng.
- **Dễ hoàn tác**: cả tính năng nằm sau một merge commit, có thể
  `git revert -m 1` bằng một lệnh.
- **Tạo thói quen cho làm việc nhóm**: khi có partner/CI (Lab 02, 05),
  branch protection sẽ chặn push thẳng lên `master`; tập quy trình
  nhánh → PR → merge ngay từ khi làm một mình giúp không phải đổi cách làm.
- **Một nhánh, một mục đích**: tên nhánh `refactor/apply-release-flow` nói
  lên mục đích thay đổi, đúng quy tắc của Release Flow.
