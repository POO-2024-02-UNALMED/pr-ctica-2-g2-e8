from classes.WithId import WithId
from .DocumentType import DocumentType

class Customer(WithId):
    def __init__(
        self,
        email: str,
        password: str,
        document_type: DocumentType,
        document_number: int,
    ) -> None:
        super().__init__(WithId.create_id(email, password))
        self.email = email
        self.password = password
        self.document_type = document_type
        self.document_number = document_number

    def get_email(self) -> str:
        return self.email

    def get_document_type(self) -> DocumentType:
        return self.document_type

    def get_document_number(self) -> int:
        return self.document_number
