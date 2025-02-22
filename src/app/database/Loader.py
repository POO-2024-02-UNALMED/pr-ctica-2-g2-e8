import os
from datetime import datetime, timedelta
from app.classes.customers.Admin import Admin
from app.classes.customers.Customer import Customer
from app.classes.customers.DocumentType import DocumentType
from app.classes.customers.User import User
from app.classes.gateways.Gateway import Gateway
from app.classes.gateways.GatewaysFactory import GatewaysFactory
from app.classes.gateways.IGateway import IGateway
from app.classes.plans import Subscription, Plan
from app.classes.transactions.Card import Card
from app.database import Repository


class Loader:
    def __init__(self, email: str, password: str, debug_mode: bool) -> None:
        self.email = email
        self.password = password
        self.system_user = None
        self.system_admin = None
        self.debug_mode = debug_mode
        self.plans = []

    def create_random_users(self) -> None:
        for i in range(10):
            user = User(
                f"jdoe{i}@gmail.com",
                f"password{i}",
                DocumentType.CC,
                f"1234567890{i}",
                Gateway.PROJECT_GATEWAY,
            )
            card = GatewaysFactory.get_gateway(Gateway.PROJECT_GATEWAY).add_credit_card(
                "5434567890111213", user.get_email(), "02/35", "123", user
            )
            user.add_credit_card(card)
            user.add_subscription(self.plans[i % 4])
            Repository.save(user)

    def load_data(self) -> None:
        Repository.set_debug_mode(self.debug_mode)
        Repository.create_temp_directory()
        advanced = Plan("Advanced", "Books, Music, Videos", 100)
        smart = Plan("Smart", "Books, Music", 80)
        basic = Plan("Basic", "Videos", 50)
        essential = Plan("Essential", "Music", 50)
        self.plans = [advanced, smart, basic, essential]
        Repository.save(advanced)
        Repository.save(smart)
        Repository.save(basic)
        Repository.save(essential)

        admin = Admin(self.email, self.password, DocumentType.CC, "1234567890")
        user = User(
            admin.get_email(),
            self.password,
            DocumentType.CC,
            admin.get_document_number(),
            Gateway.PROJECT_GATEWAY,
        )

        Repository.save(admin)
        admin.configure_gateway(Gateway.PROJECT_GATEWAY, "publicKey", "privateKey")
        GatewaysFactory.initialize_gateway(Gateway.PROJECT_GATEWAY)
        project_gateway = GatewaysFactory.get_gateway(Gateway.PROJECT_GATEWAY)

        card = project_gateway.add_credit_card(
            "5434567890111213", user.get_email(), "02/35", "123", user
        )
        card2 = project_gateway.add_credit_card(
            "454567890114312", user.get_email(), "10/30", "132", user
        )
        user.add_credit_card(card)
        user.add_credit_card(card2)

        user.add_subscription(essential, card2)
        future_subscription = Subscription(
            user, basic, datetime.now().date() + timedelta(days=1)
        )

        Repository.save(future_subscription, f"Subscription{os.sep}{basic.get_name()}")
        Repository.save(user)
        self.system_user = user
        self.system_admin = admin
        self.create_random_users()

    @staticmethod
    def load_customer(email: str, password: str, type: str) -> Customer:
        return Repository.load(type, Customer.create_id(email, password))

    def get_system_user(self) -> User:
        return self.system_user

    def get_system_admin(self) -> Admin:
        return self.system_admin
