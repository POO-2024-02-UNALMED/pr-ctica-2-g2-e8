from database.Repository import Repository

class Authenticate:
    def __init__(self, gateway):
        credential = Repository.load("Credential", gateway.get_name())
        self.AUTHENTICATION_TOKEN = credential.get_public_key() + credential.get_private_key()

    def get_authentication_token(self):
        return self.AUTHENTICATION_TOKEN