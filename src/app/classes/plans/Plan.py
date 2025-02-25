from __future__ import annotations

from app.classes import WithId
from .PlanStatus import PlanStatus
from app.database import Repository

from typing import cast

from multimethod import multimethod


class Plan(WithId):

    @multimethod
    def __init__(self, name: str, description: str, price: float) -> None:
        super().__init__(name)
        self._name = name
        self._description = description
        self._price = price
        self._status = PlanStatus.ACTIVE

    @multimethod
    def __init__(
        self, name: str, description: str, price: float, status: PlanStatus
    ) -> None:
        super().__init__(name)
        self._name = name
        self._description = description
        self._price = price
        self._status = status

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_price(self) -> float:
        return self._price

    @staticmethod
    def get_all() -> list[Plan]:
        with_id_list = Repository.load_all_object_in_directory("Plan")
        return [
            _plan
            for _plan in with_id_list
            if isinstance(_plan, Plan) and _plan.get_status() == PlanStatus.ACTIVE
        ]

    @staticmethod
    def get_inactive_plans() -> list[Plan]:
        with_id_list = Repository.load_all_object_in_directory("Plan")
        return [
            plan
            for plan in with_id_list
            if isinstance(plan, Plan) and plan.get_status() == PlanStatus.INACTIVE
        ]

    @staticmethod
    def get_plan(name) -> Plan | None:
        if plan := Repository.load("Plan", name):
            return cast(Plan, plan)

        return None

    def get_status(self) -> PlanStatus:
        return self._status

    def set_status(self, status: PlanStatus) -> None:
        self._status = status

    def __str__(self) -> str:
        return f"Plan: {self._name}, Description: {self._description}, Price: {self._price}, Status: {self._status}"
