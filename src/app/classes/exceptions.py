class AppException(Exception):
    def __init__(self, msg: str) -> None:
        """ Base exception for application """
        super().__init__(f"Application error handler: {msg}")

class InvalidInputType(AppException):
    def __init__(self, msg: str) -> None:
        """ Exception to control if input value is not of the correct type """
        super().__init__(f"Invalid argument type: {msg}")

class InputValueNotProvided(AppException):
    def __init__(self, input_label: str) -> None:
        """ Exception to control if input value is not provided """
        super().__init__(f"Input {input_label} required")
