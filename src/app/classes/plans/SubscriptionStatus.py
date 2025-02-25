from enum import StrEnum

class SubscriptionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
