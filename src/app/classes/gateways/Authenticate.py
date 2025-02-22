from app.database.Repository import Repository
from app.classes.gateways import Gateway, Credential
from typing import cast

class Authenticate:
    def __init__(self, gateway: Gateway):
        credential = Repository.load("Credential", gateway.value)
        if not credential:
            self.AUTHENTICATION_TOKEN = None
            return

        credential = cast(Credential, credential)
        self.AUTHENTICATION_TOKEN = credential.get_public_key() + credential.get_private_key()

    def get_authentication_token(self) -> str | None:
        return self.AUTHENTICATION_TOKEN
