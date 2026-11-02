# Lab 02 – Trả lời câu hỏi thảo luận

Sinh viên: Lê Thu Ngân – MSSV 202417257

## Ghi chú về cách làm (làm một mình)

- Branch protection cho `master`: Require a pull request, **Require approvals = 0**
  (theo hướng dẫn cho trường hợp làm một mình), Dismiss stale approvals,
  Do not allow bypassing.
- "Dev 2" được mô phỏng bằng bản clone thứ hai `aims-dev2`.
- GitHub không cho tác giả tự *Approve* / *Request changes* PR của mình, nên ở
  PR #4 (`feature/cart-print`) bước review được thực hiện bằng review comment
  trên dòng `def print_cart` ("Nếu giỏ hàng trống thì nên in 'The cart is
  empty'") → sửa trên cùng nhánh (`feat: handle empty cart in print_cart`) →
  trả lời và *Resolve conversation* → merge.

## So sánh 3 kiểu merge (quan sát trên lịch sử thật)

```
* fd0334a docs: add use case diagram          ← Rebase and merge (PR #6)
* c134d2c feat: add search_by_title (#5)      ← Squash and merge (PR #5)
*   d9c2282 Merge pull request #4 ...         ← Merge commit (PR #4)
|\
| * 9c48a6d feat: handle empty cart in print_cart
| * 772747f feat: show cart details in demo program
| * d8af35a feat: add print_cart to Cart
```

| | Merge commit | Squash | Rebase |
|---|---|---|---|
| Giữ commit chi tiết | ✔ | ✘ (gộp thành 1) | ✔ (nhưng SHA mới: `9327ad5` → `fd0334a`) |
| Lịch sử tuyến tính | ✘ | ✔ | ✔ |
| Revert cả tính năng | 1 lệnh (`git revert -m 1`) | 1 lệnh | phải revert nhiều commit |

## 1. Vì sao phải đồng bộ `master` trước khi gửi PR?

- Nhánh `feature/search-by-title` được tạo từ `master` cũ, khi chưa có
  `print_cart`. Thứ được review phải là thứ sẽ được tích hợp: merge
  `origin/master` vào nhánh rồi chạy lại `python main.py` giúp kiểm tra **kết
  quả tích hợp thật** (mã mới + mã người khác vừa merge) ngay trên nhánh,
  trước khi vào `master`.
- Xung đột (nếu có) được giải quyết bởi tác giả nhánh – người hiểu thay đổi
  của mình nhất – trên nhánh riêng, không làm hỏng `master`.
- `master` luôn ở trạng thái chạy được; nhánh sống ngắn, gần `master`, tránh
  "merge hell".

## 2. Khi nào không được rebase?

- **Không rebase các commit đã chia sẻ** (đã push và người khác có thể đã dựa
  vào), đặc biệt là `master` và `release/*`. Rebase tạo commit mới với SHA mới
  (như `9327ad5` → `fd0334a`), buộc phải `push --force`, làm lịch sử của người
  khác lệch, có thể mất commit của họ.
- Không rebase nhánh mà người khác đang cùng làm hoặc đã tạo nhánh con từ nó.
- Chỉ rebase nhánh riêng, chưa ai dùng; nếu buộc phải đẩy lại thì dùng
  `git push --force-with-lease` thay cho `--force`.
- Không nên rebase khi cần giữ đúng bối cảnh lịch sử của một lần tích hợp
  (ví dụ một merge commit đánh dấu tính năng để có thể `revert -m 1`).

## 3. `feature/*` khác `topic/*` ra sao?

| | `feature/*` | `topic/*` |
|---|---|---|
| Nội dung | Một **tính năng** của sản phẩm, thay đổi hành vi người dùng thấy | Một **chủ đề** không phải tính năng: tài liệu, cấu hình, quy trình, chuẩn bị phát hành |
| Ví dụ trong bài | `feature/cart-print`, `feature/search-by-title` | `topic/pr-template`, `topic/use-case-diagram` |
| Ghi vào CHANGELOG | Thường có (mục *Added*) | Thường không |
| Commit type | `feat:` | `docs:`, `chore:`, `ci:`… |

Cả hai đều tạo từ `master`, merge về `master` qua PR và xóa sau khi merge.
