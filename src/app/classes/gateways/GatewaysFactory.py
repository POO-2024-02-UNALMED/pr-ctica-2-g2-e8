from .ProjectGateway import ProjectGateway

class GatewaysFactory:
    def __init__(self, gateway):
        self.gateways = {}
        self.gateway = gateway
        self.initialize_gateway()

    def __init__(self, gatewaysToAdd):
        self.gateways = {}
        self.iterate_and_add(gatewaysToAdd)

    def iterate_and_add(self, gatewaysToAdd):
        for gateway in gatewaysToAdd:
            self.gateways[gateway] = ProjectGateway()

    def get_gateway(self, gateway):
        return self.gateways.get(gateway)

    def initialize_gateway(self, gateway):
        if not self.gateways:
            self.gateways[gateway] = ProjectGateway()
        else:
            self.gateways[gateway] = ProjectGateway()

    def initialize_gateways(self, gatewaysAndCredentials):
        if not self.gateways:
            self.iterate_and_add(gatewaysAndCredentials)
        else:
            self.iterate_and_add(gatewaysAndCredentials)