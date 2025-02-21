from app.classes.exceptions import AppException


class NoInRange(AppException):
    def __init__(
        self, key: str, min: int | float | None, max: int | float | None
    ) -> None:
        """Exception to control if input value is not in range"""
        if min == max:
            super().__init__(f"Value of {key} should be {min}")
        elif min is None:
            super().__init__(f"Value of {key} should be less than {max}")
        else:
            super().__init__(f"Value of {key} should be greater than {min}")
