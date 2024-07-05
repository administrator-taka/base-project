class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseCommonError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
