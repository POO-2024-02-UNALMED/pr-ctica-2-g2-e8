from app.classes.exceptions import AppException


class LengthException(AppException):
    def __init__(self, key: str, min_len: int, max_len: int) -> None:
        """Exception to control if input value is not of the correct length"""
        super().__init__(
            f"{key} must have between {min_len} and {max_len} characters"
            if min_len != max_len
            else f"length of {key} must be {min_len}"
        )
