def search_by_title(items, keyword):
    """Trả về danh sách DVD có tiêu đề chứa keyword."""
    return [dvd for dvd in items if keyword in dvd.title]
