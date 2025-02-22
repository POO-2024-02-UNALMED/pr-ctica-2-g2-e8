from .Customer import Customer
from ..plans.Plan import Plan
from ..gateways.Credential import Credential
from ...database.Repository import Repository

class Admin(Customer):
    def __init__(self, email, password, document_type, document_number) -> None:
        super().__init__(email, password, document_type, document_number)

    def create_plan(self, name, description, price):
        plan = Plan(name, description, price)
        Repository.save(plan)
        return plan

    def configure_gateway(self, gateway, public_key, private_key):
        credential = Credential(public_key, private_key, gateway)
        Repository.save(credential)
        return credential

    def inactivate(self, plan):
        Repository.update(plan)