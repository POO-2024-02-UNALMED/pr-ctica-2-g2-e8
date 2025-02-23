from app.classes.gateways import IGateway, Gateway


class GatewaysFactory:
    gateways: dict[Gateway, IGateway] = {}

    def __init__(self) -> None:
        raise NotImplementedError("This class should not be instantiated")

    @classmethod
    def initialize_gateways(cls, gateways_to_add: list[IGateway]) -> None:
        for gateway in gateways_to_add:
            cls.initialize_gateway(gateway)

    @classmethod
    def get_gateway(cls, gateway: Gateway) -> IGateway:
        return cls.gateways.get(gateway)

    @classmethod
    def initialize_gateway(cls, gateway: IGateway) -> IGateway:
        if not cls.gateways.get(gateway.get_name()):
            cls.gateways[gateway.get_name()] = gateway

        return cls.gateways[gateway.get_name()]
