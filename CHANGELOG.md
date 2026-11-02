# Changelog

Mọi thay đổi đáng chú ý của AIMS-mini được ghi lại trong tệp này.

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

### Added
- `Cart.sort_by_title()`, `Cart.sort_by_cost()`: sắp xếp giỏ hàng theo tiêu đề / theo giá
- `search_by_category()` trong `aims/search.py`: tìm đĩa theo thể loại

## [1.0.0] - 2026-11-02

### Added
- `Cart.print_cart()`: in danh sách đĩa và tổng tiền; giỏ trống in "The cart is empty"
- `search_by_title()` trong `aims/search.py`: tìm đĩa theo tiêu đề
- `Cart.total_cost_with_discount(percent)`: tổng tiền sau giảm giá, `percent` ngoài [0, 100] → `ValueError`
- Thông báo tiếng Việt khi thêm đĩa vào giỏ
- Bộ kiểm thử `unittest` (`tests/test_cart.py`, `tests/test_discount.py`)
- Tài liệu: PR template, sơ đồ use case
- Chương trình in phiên bản khi khởi động (`AIMS-mini v1.0.0`)

### Fixed
- Giỏ hàng nhận đĩa thứ 21 dù giới hạn là 20 (#8)
- `total_cost_with_discount` trả về số tiền được giảm thay vì tổng sau giảm (#10)

### Removed
- Hiển thị tiêu đề đĩa khi thêm vào giỏ (đã hoàn tác ở #14)

## [0.3.0] - 2026-11-02
Lab 03: bugfix flow, xung đột, hoàn tác.

## [0.2.0] - 2026-11-02
Lab 02: feature/topic flow, Pull Request, 3 kiểu merge.

## [0.1.0] - 2026-11-02
Lab 01: mã nguồn ban đầu, refactor vào package `aims`.

[Unreleased]: https://github.com/thunganle272/it3180-202417257-aims/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/thunganle272/it3180-202417257-aims/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/thunganle272/it3180-202417257-aims/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/thunganle272/it3180-202417257-aims/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/thunganle272/it3180-202417257-aims/releases/tag/v0.1.0
