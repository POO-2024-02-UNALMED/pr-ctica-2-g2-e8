from app.classes.exceptions import AppException

class InvalidInputType(AppException):
    def __init__(self, msg: str) -> None:
        """ Exception to control if input value is not of the correct type """
        super().__init__(f"Invalid argument type: {msg}")