# Lab 05 – Trả lời câu hỏi thảo luận

Sinh viên: Lê Thu Ngân – MSSV 202417257

## Kết quả thực hành

- Phần A: `feature/search-by-category` (PR #19, hàm đặt **phía trên**
  `search_by_title`) → `topic/prepare-release-1.1.0` (PR #20) → tạo
  `release/lab05` (chưa gắn tag).
- Phần B: tái hiện lỗi trên worktree `v1.0.0`: `search_by_title([D('The Lion King')], 'lion')` → `[]`.
  Issue **#21** "search_by_title is case-sensitive (affects v1.0.0)" (slide ghi #20).
- Phần C: `hotfix/search-case-insensitive` từ `origin/release/lab04`
  - Commit 1 (`FIX_SHA = 2f736cd`): `fix: make search_by_title case-insensitive` (Refs #21) – chỉ `search.py` + `test_search.py`
  - Commit 2: `chore: bump version to 1.0.1` – `__init__.py` + `CHANGELOG.md`
  - PR #22 base `release/lab04`, Files changed đúng 4 tệp → merge → tag `v1.0.1`. Issue #21 vẫn mở.
- Phần D: `hotfix/search-case-insensitive-master`: `cherry-pick -x 2f736cd` → 8 tests OK →
  `docs: add 1.0.1 to changelog` → PR #23 (`Fixes #21`) → Issue #21 tự đóng.
- Phần E: `hotfix/search-case-insensitive-lab05` từ `origin/release/lab05`:
  `cherry-pick -x 2f736cd` → PR #24 base `release/lab05` → tag `v1.1.0`.
- Phần F:
  ```
  $ git log --all --oneline --grep "cherry picked from commit 2f736cd"
  75878a0 fix: make search_by_title case-insensitive   # release/lab05
  da8c944 fix: make search_by_title case-insensitive   # master
  $ git tag --contains 2f736cd
  v1.0.1
  $ git cherry -v origin/master origin/release/lab04
  - 2f736cd fix: make search_by_title case-insensitive   # master đã có bản tương đương
  + dbc84bd chore: bump version to 1.0.1                 # chưa có – đúng chủ đích
  $ (vòng lặp kiểm tra hành vi)
  v1.0.1   1
  v1.1.0   1
  master   1
  $ git diff --stat v1.0.0 v1.0.1   # 4 tệp
  ```
- Mở rộng CI: `.github/workflows/ci.yml` (PR #25, job `test` pass);
  `bugfix/ci-demo` cố ý làm hỏng `total_cost` → PR #26 job `test` **fail** (không merge).
  Sau khi bật *Require status checks to pass* (`test`) cho `master`, PR #26 chuyển
  sang `mergeStateStatus: BLOCKED` → nút Merge bị khóa; PR được đóng, không merge.

## Vì sao ở Phần A chưa gắn tag v1.1.0?

Tag đánh dấu baseline **đã phát hành**, đã chia sẻ thì không được xóa/di chuyển.
Khi tạo `release/lab05` ta đã biết lỗi có thể ảnh hưởng (lỗi có từ Lab 02);
nếu gắn `v1.1.0` sớm thì bản 1.1.0 đã phát hành **chứa lỗi**, và bản sửa phải
phát hành thành `v1.1.1`. Chờ đưa bản sửa vào `release/lab05` rồi mới gắn tag
giúp `v1.1.0` là bản đúng ngay từ đầu.

## Vì sao không merge cả nhánh hotfix vào master?

Nhánh hotfix có 2 commit; commit 2 đặt `__version__ = "1.0.1"`, trong khi
`master` đang là `1.1.0` → xung đột và làm sai phiên bản của master. Chỉ commit
sửa lỗi cần lan truyền, nên dùng `cherry-pick -x <FIX_SHA>` (giữ truy vết
`(cherry picked from commit ...)`). Đây cũng là lý do commit sửa lỗi chỉ chứa
mã sửa lỗi, số phiên bản tách sang commit riêng.

## 1. Ưu, nhược điểm của *upstream first* so với *release first*

**Upstream first** (Release Flow của Microsoft): sửa trên `master` trước, rồi
cherry-pick xuống các `release/*`.

| | Upstream first | Release first (học phần) |
|---|---|---|
| Ưu | Không bao giờ quên sửa master → lỗi không tái xuất ở bản sau ("regression"); bản sửa được review/test trên dòng chính, CI đầy đủ; master là nguồn sự thật duy nhất | Sửa ngay trên đúng mã đang chạy của bản đã phát hành → nhanh, ít rủi ro cho người dùng đang gặp lỗi; tái hiện và kiểm thử đúng phiên bản bị lỗi; phù hợp khi master đã khác xa bản phát hành |
| Nhược | Master có thể đã thay đổi nhiều → bản sửa trên master không áp dụng sạch vào release cũ (cherry-pick xung đột, phải viết lại); chậm hơn khi cần vá khẩn cấp | Dễ **quên lan truyền** về master/các release khác → lỗi quay lại ở bản sau; phải cherry-pick "ngược" lên, cũng có thể xung đột; cần kiểm toán (Phần F) để chắc chắn đủ mọi dòng |

## 2. Nếu quên lan truyền bản sửa sang `release/lab05`, lệnh nào ở Phần F phát hiện?

- **Vòng lặp kiểm tra hành vi** trên `v1.0.1`, `v1.1.0`, `master` sẽ in `0`
  cho `v1.1.0` (tìm "lion" không ra) – phát hiện trực tiếp nhất.
- `git log --all --oneline --grep "cherry picked from commit <FIX_SHA>"` chỉ ra
  **1** bản cherry-pick (master) thay vì 2.
- `git cherry -v origin/release/lab05 origin/release/lab04` sẽ hiện
  `+ <FIX_SHA> fix: ...` (dấu `+`: release/lab05 chưa có bản tương đương).
- `git branch -a --contains <sha-cherry-pick>` / so sánh nội dung
  `git show v1.1.0:aims/search.py` cũng cho thấy dòng chưa sửa.
