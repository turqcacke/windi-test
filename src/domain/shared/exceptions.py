class DomainExecption(Exception):
    def __init__(self, message: str | None = None, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)
