class PaginationInfo:
    def __init__(self, paginator, page, page_size):
        self.paginator = paginator
        self.page = page
        self.page_size = page_size

    @property
    def total(self):
        return self.paginator.count

    @property
    def total_pages(self):
        return self.paginator.num_pages

    def to_dict(self):
        return {
            'total': self.total,
            'page': self.page,
            'page_size': self.page_size,
            'total_pages': self.total_pages
        }
