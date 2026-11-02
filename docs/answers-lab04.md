# Lab 04 – Trả lời câu hỏi thảo luận

Sinh viên: Lê Thu Ngân – MSSV 202417257

## Kết quả thực hành

- Annotated tag (`git tag -n`):
  `v0.1.0 Lab 01 release` · `v0.2.0 Lab 02 release` · `v0.3.0 Lab 03 release` ·
  `v1.0.0 AIMS-mini 1.0.0 - Lab 04 release`.
- `v1.0.0` trùng đầu `release/lab04` (`31fcbbd`) tại thời điểm phát hành
  (sau hotfix Lab 05, đầu nhánh là `3db10ec` = `v1.0.1`; tag `v1.0.0` không di chuyển).
- Rule `release/*`: Require PR, no bypass, ✘ force push, ✘ deletion. Push thẳng bị chặn:
  ```
  $ git push origin HEAD:release/lab04
  remote: error: GH006: Protected branch update failed for refs/heads/release/lab04.
  remote: - Changes must be made through a pull request.
   ! [remote rejected] HEAD -> release/lab04 (protected branch hook declined)
  ```
- GitHub Release: https://github.com/thunganle272/it3180-202417257-aims/releases/tag/v1.0.0
  (tag có sẵn `v1.0.0`, nội dung mục `[1.0.0]` của CHANGELOG + generated release notes).
- Status accounting:
  - `git log --oneline release/lab04..master` → `feat: add sort_by_title and sort_by_cost to Cart` + merge PR #17
  - `git log --oneline master..release/lab04` → **rỗng** (release không có gì master không có)
  - `git diff --stat v0.3.0 v1.0.0` → `CHANGELOG.md`, `aims/__init__.py`, `main.py`
  - `git diff --stat v1.0.0 master` → `CHANGELOG.md`, `aims/cart.py`, `tests/test_sort.py`
  - `git describe --tags` trên master → `v1.0.0-2-g086d7e4` (2 commit sau v1.0.0)
- Tái tạo: `git switch --detach v0.2.0 && python main.py` → `Total cost: 63.89 $`;
  `git worktree add ../aims-v1.0.0 v1.0.0` → 4 tests OK, dòng đầu `AIMS-mini v1.0.0`;
  `git archive ... -o ../aims-1.0.0.zip v1.0.0`.
- Kiểm toán v1.0.0: `git show v1.0.0:aims/__init__.py` → `__version__ = "1.0.0"`;
  `git ls-tree -r --name-only v1.0.0` không có `__pycache__/` hay tệp rác.
- `sort_by_cost` có trên `master`, **không** có trên `release/lab04`.

## Vì sao chuẩn bị phát hành trên master trước, không sửa trên nhánh release?

- `release/*` là ảnh chụp đóng băng của `master`; nếu sửa phiên bản/CHANGELOG
  trực tiếp trên release thì `master` không có thay đổi đó, và vì release không
  bao giờ merge ngược về master nên thay đổi bị "kẹt" lại, lần phát hành sau lại
  thiếu.
- Chuẩn bị qua PR trên `master` → được review, lịch sử chung có ghi nhận;
  sau đó `release/lab04` tạo ra đã đúng ngay từ đầu, không cần commit thêm.

## 1. Vì sao `release/*` không merge vào `master`?

- Trong Release Flow, `master` là dòng phát triển chính, **mọi thay đổi đi vào
  `master` trước** rồi mới được cắt ra thành `release/*`. Vì vậy release chỉ
  chứa những gì master đã có (`git log master..release/lab04` rỗng) – không có
  gì cần merge ngược.
- Những commit chỉ thuộc riêng một dòng phát hành (ví dụ `chore: bump version
  to 1.0.1` ở Lab 05) **không được** vào master; merge cả nhánh release sẽ kéo
  theo chúng và gây xung đột phiên bản (1.0.1 vs 1.1.0 trên master).
- Bản sửa lỗi cần có ở cả hai nơi được lan truyền có chọn lọc bằng
  `cherry-pick -x`, giữ truy vết nguồn gốc.
- Giữ lịch sử master gọn, release là các nhánh "lá" độc lập, dễ bảo trì song song.

**So sánh với GitFlow:**

| | Release Flow (học phần) | GitFlow |
|---|---|---|
| Nhánh chính | `master` (phát triển + nguồn phát hành) | `develop` (phát triển) + `main` (chỉ bản phát hành) |
| Nhánh release | Cắt từ `master`, sống lâu để bảo trì, **không merge lại** | Cắt từ `develop`, khi xong **merge vào cả `main` và `develop`** rồi xóa |
| Hotfix | Từ `release/*`, cherry-pick sang `master` | Từ `main`, merge vào `main` và `develop` |
| Phù hợp | Nhiều phiên bản song song, phát hành theo đợt | Phát hành định kỳ, một bản đang được hỗ trợ |
| Độ phức tạp | Ít nhánh dài hạn, ít merge | Nhiều nhánh dài hạn, nhiều merge hai chiều |

## 2. Vì sao lên 1.0.0 mà không phải 0.4.0?

- Theo SemVer, `0.y.z` là giai đoạn phát triển ban đầu, API chưa ổn định, có
  thể thay đổi bất kỳ lúc nào (v0.1.0…v0.3.0 tương ứng Lab 01–03).
- `1.0.0` là **bản phát hành công khai đầu tiên**, cam kết API công khai
  (`Cart.add_dvd`, `print_cart`, `total_cost_with_discount`, `search_by_title`…)
  đã ổn định. Từ đây số phiên bản mang ý nghĩa tương thích: sửa lỗi → PATCH
  (1.0.1), thêm tính năng tương thích → MINOR (1.1.0), phá vỡ tương thích → MAJOR.
- Lab 04 là lần đầu có quy trình phát hành đầy đủ (CHANGELOG, tag, release
  được bảo vệ, GitHub Release) và có người dùng cần bảo trì (hotfix ở Lab 05),
  nên là thời điểm hợp lý để lên 1.0.0. Nếu vẫn là 0.4.0 thì không thể dùng
  đúng ngữ nghĩa PATCH cho bản vá hotfix.
