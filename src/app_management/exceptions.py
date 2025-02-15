class ErrorAplicacion(Exception):
    """Exception to control if acceptance is not valid"""

    def __init__(self, msg: str) -> None:
        super().__init__(f"Manejo de errores de la Aplicación: {msg}")

class InvalidParameter(ErrorAplicacion):
    def __init__(self) -> None:
        msg = "Parámetro inválido"
        super().__init__(msg)
