from app.classes.WithId import WithId
from app.classes.gateways.Gateway import Gateway

class Credential(WithId):
    def __init__(self, public_key: str, private_key: str, gateway: Gateway):
        super().__init__(gateway.value)
        self.public_key = public_key
        self.private_key = private_key
        self.gateway = gateway

    def get_public_key(self) -> str:
        return self.public_key

    def get_private_key(self) -> str:
        return self.private_key

    def get_gateway(self) -> Gateway:
        return self.gateway
