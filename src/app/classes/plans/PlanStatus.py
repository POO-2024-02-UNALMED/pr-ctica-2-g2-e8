from enum import Enum

class PlanStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
