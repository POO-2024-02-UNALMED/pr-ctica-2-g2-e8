import os
from datetime import datetime, timedelta
from app.classes.customers.Admin import Admin
from app.classes.customers.Customer import Customer
from app.classes.customers.DocumentType import DocumentType
from app.classes.customers.User import User
from app.classes.gateways import Gateway, IGateway
from app.classes.gateways import GatewaysFactory, ProjectGateway
from app.classes.plans import Subscription, Plan
from app.classes.plans.PlanStatus import PlanStatus
from app.database import Repository


class Loader:
    def __init__(self, email: str, password: str, debug_mode: bool) -> None:
        self._admin = Admin(email, password, DocumentType.CC, "1234567890")
        self._user = User(
            email,
            password,
            DocumentType.CC,
            "1234567890",
            Gateway.PROJECT_GATEWAY,
        )
        self.debug_mode = debug_mode
        self.plans = []
        self._gateway: IGateway | None = None

    def create_random_users(self) -> None:
        for i in range(10):
            user = User(
                f"jdoe{i}@gmail.com",
                f"password{i}",
                DocumentType.CC,
                f"1234567890{i}",
                Gateway.PROJECT_GATEWAY,
            )
            card = self._gateway.add_credit_card(
                "5434567890111213", user.get_email(), "02/35", "123", user
            )
            user.add_credit_card(card)
            user.add_subscription(self.plans[i % 4], card)
            Repository.save(user)

    def load_data(self) -> None:
        Repository.set_debug_mode(self.debug_mode)
        Repository.create_temp_directory()
        advanced = Plan("Advanced", "Books, Music, Videos", 500000.0)
        smart = Plan("Smart", "Books, Music", 400000.0)
        basic = Plan("Basic", "Videos", 300000.0)
        essential = Plan("Essential", "Music", 250000.0)
        deactivated_plan = Plan(
            "Deactivated Essential", "Music", 250000.0, PlanStatus.INACTIVE
        )
        self.plans = [advanced, smart, basic, essential]
        Repository.save(advanced)
        Repository.save(smart)
        Repository.save(basic)
        Repository.save(essential)
        Repository.save(deactivated_plan)

        Repository.save(self._admin)
        self._admin.configure_gateway(
            Gateway.PROJECT_GATEWAY, "publicKey", "privateKey"
        )
        self._gateway = GatewaysFactory.initialize_gateway(ProjectGateway())

        card = self._gateway.add_credit_card(
            "5434567890111213", self._user.get_email(), "02/35", "123", self._user
        )
        card2 = self._gateway.add_credit_card(
            "454567890114312", self._user.get_email(), "10/30", "132", self._user
        )
        self._user.add_credit_card(card)
        self._user.add_credit_card(card2)

        self._user.add_subscription(essential, card2)
        self._user.add_subscription(advanced, None)

        future_subscription = Subscription(
            self._user, basic, datetime.now().date() + timedelta(days=1)
        )

        Repository.save(future_subscription, f"Subscription{os.sep}{basic.get_name()}")
        Repository.save(self._user)
        self.create_random_users()

    @staticmethod
    def load_customer(email: str, password: str, type: str) -> Customer:
        return Repository.load(type, Customer.create_id(email, password))

    def get_system_user(self) -> User:
        return self._user

    def get_system_admin(self) -> Admin:
        return self._admin
