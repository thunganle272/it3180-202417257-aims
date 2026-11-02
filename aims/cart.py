MAX_NUMBERS_ORDERED = 20


class Cart:
    """Giỏ hàng chứa tối đa MAX_NUMBERS_ORDERED đĩa DVD."""

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= MAX_NUMBERS_ORDERED:
            print("The cart is almost full")
            return False
        self.items.append(dvd)
        print("Đã thêm đĩa vào giỏ hàng")
        return True

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)
            print("The disc has been removed")
            return True
        print("The disc is not in the cart")
        return False

    def total_cost(self):
        return sum(item.cost for item in self.items)

    def sort_by_title(self):
        """Sắp xếp giỏ theo tiêu đề (A→Z), cùng tiêu đề thì giá giảm dần."""
        self.items.sort(key=lambda dvd: (dvd.title.lower(), -dvd.cost))

    def sort_by_cost(self):
        """Sắp xếp giỏ theo giá giảm dần, cùng giá thì theo tiêu đề (A→Z)."""
        self.items.sort(key=lambda dvd: (-dvd.cost, dvd.title.lower()))

    def total_cost_with_discount(self, percent):
        """Tổng tiền sau khi giảm giá percent %."""
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        return self.total_cost() * (100 - percent) / 100

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        print("***********************CART***********************")
        print("Ordered Items:")
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item}")
        print(f"Total cost: {self.total_cost():.2f} $")
        print("***************************************************")
