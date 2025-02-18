class AppException(Exception):
    def __init__(self, msg: str) -> None:
        """ Base exception for application """
        super().__init__(f"Application error handler: {msg}")
