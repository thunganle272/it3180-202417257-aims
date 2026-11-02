# Lab 03 – Trả lời câu hỏi thảo luận

Sinh viên: Lê Thu Ngân – MSSV 202417257

## Ghi chú về cách làm

- Issue báo lỗi là **#8** (Issue và PR dùng chung dãy số trên GitHub nên không
  phải #6 như ví dụ trong slide). Commit `test: reproduce cart limit bug (#8)`
  đứng **trước** `fix: reject DVDs beyond MAX_NUMBERS_ORDERED` (thân: `Fixes #8`);
  PR #9 merge vào `master` → Issue #8 tự đóng.
- Bugfix từ nhánh tính năng: PR #10 `bugfix/discount-calculation` có
  **base `feature/discount`**, sau đó PR #11 đưa `feature/discount` vào `master`.
- Xung đột: PR #12 (`feature/vietnamese-messages`) merge trước, PR #13
  (`feature/show-added-title`) báo *CONFLICTING*; giải quyết bằng cách 1
  (`git merge origin/master`), kết hợp thành
  `print(f"Đã thêm đĩa '{dvd.title}' vào giỏ hàng")`, chạy test rồi mới commit.
- Hoàn tác trên nhánh nháp `topic/undo-practice` (KHÔNG push), commit tập dượt
  `chore: undo practice commit` (thêm `undo-note.txt`):
  ```
  $ git reset --soft HEAD~1     # status: "A  undo-note.txt"  → thay đổi về STAGING
  $ git reset --mixed HEAD~1    # status: "?? undo-note.txt"  → thay đổi về WORKING DIR
  $ git reset --hard HEAD~1     # HEAD is now at fde6bf5; undo-note.txt biến mất
  $ git reflog -2
  fde6bf5 HEAD@{0}: reset: moving to HEAD~1
  1a41a3b HEAD@{1}: checkout: moving from master to topic/undo-practice
  $ git reset --hard 1a41a3b    # tìm lại commit "đã mất" → undo-note.txt quay lại
  ```
  Sau đó xóa nhánh nháp (`git branch -D topic/undo-practice`).
- Hoàn tác lịch sử chung: PR #14 `git revert -m 1 fde6bf5` (merge commit của PR #13).
- `master` hiện có 4 tests OK.

## 1. Merge base là gì?

- Merge base là **commit tổ tiên chung gần nhất** của hai nhánh – điểm mà hai
  nhánh tách ra. Xem bằng `git merge-base A B`.
- Ví dụ trong repo: `git merge-base f6a79ff bea0b0e` → `3115c92` (master sau
  PR #11), là nơi cả `feature/vietnamese-messages` và `feature/show-added-title`
  được tạo ra.
- Git dùng **three-way merge**: so sánh merge base với đầu mỗi nhánh.
  - Chỉ một bên sửa một vùng → Git tự lấy bản đã sửa.
  - Cả hai bên cùng sửa **cùng một vùng** so với merge base (dòng `print` trong
    `add_dvd`) → Git không biết chọn bên nào → **conflict**, người phát triển
    phải kết hợp ý đồ của cả hai.
- Nhánh sống càng lâu, merge base càng cũ, khả năng xung đột càng cao → nên
  đồng bộ `master` thường xuyên.

## 2. Vì sao `master`/`release/*` phải dùng revert?

| | `reset` | `revert` |
|---|---|---|
| Cơ chế | Dời con trỏ nhánh về commit cũ → **viết lại lịch sử** | Tạo **commit mới** đảo ngược thay đổi |
| Cần force push | Có | Không |
| Dùng cho | Commit chưa push (nhánh nháp `topic/undo-practice`) | `master`, `release/*` |

- `master` và `release/*` là lịch sử **đã chia sẻ**: người khác đã pull, đã tạo
  nhánh từ đó; `release/*` còn là baseline đã giao. `reset` + `push --force` sẽ
  xóa commit mà người khác đang dựa vào, làm lệch bản sao của họ và có thể mất
  công việc (chỉ còn cứu được bằng `reflog` trên máy có commit).
- Branch protection chặn force push lên các nhánh này, và mọi thay đổi phải qua
  PR → `revert` phù hợp vì nó là một thay đổi bình thường, được review, có
  commit ghi lại *ai hoàn tác, khi nào, vì sao* (truy vết – status accounting).
- Với merge commit phải dùng `git revert -m 1 <sha>` để chỉ rõ parent 1
  (nhánh `master`) là dòng chính cần giữ lại.
- Lưu ý: sau khi revert một merge, muốn đưa lại tính năng thì phải *revert cái
  revert*, vì Git coi các commit của nhánh đó đã được merge rồi.
