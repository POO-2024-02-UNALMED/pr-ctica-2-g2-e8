from app.classes.gateways import IGateway, Gateway

class GatewaysFactory:
    def __init__(self, gateways_to_add: list[IGateway]) -> None:
        self.gateways: dict[Gateway, IGateway] = {}
        self.iterate_and_add(gateways_to_add)

    def iterate_and_add(self, gateways_to_add: list[IGateway]) -> None:
        for gateway in gateways_to_add:
            self.initialize_gateway(gateway)

    def get_gateway(self, gateway: Gateway) -> IGateway:
        return self.gateways.get(gateway)

    def initialize_gateway(self, gateway: IGateway) -> None:
        if not self.gateways.get(gateway.get_name()):
            self.gateways[gateway.get_name()] = gateway
