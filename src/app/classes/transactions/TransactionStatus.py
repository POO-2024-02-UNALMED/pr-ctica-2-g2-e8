from enum import Enum

class TransactionStatus(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    REVERSED = "REVERSED"