from app.classes.exceptions import AppException

class InputValueNotProvided(AppException):
    def __init__(self, input_label: str) -> None:
        """ Exception to control if input value is not provided """
        super().__init__(f"Input {input_label} required")
