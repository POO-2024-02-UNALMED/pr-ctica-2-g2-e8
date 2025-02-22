from classes.WithId import WithId

class Credential(WithId):
    def __init__(self, public_key, private_key, gateway):
        super().__init__(gateway.get_name())
        self.public_key = public_key
        self.private_key = private_key
        self.gateway = gateway

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_gateway(self):
        return self.gateway
