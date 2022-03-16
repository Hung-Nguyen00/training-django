from enum import Enum


class OrderStatus(str, Enum):
    APPROVED    = "Approved"
    IS_SHIPPING = "Is shipping"
    CANCELLED   = "Cancelled"
    DONE        = "Done"
    REFUNDED    = "Refunded"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)