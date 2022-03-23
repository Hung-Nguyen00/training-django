from enum import Enum


class OrderStatus(str, Enum):
    APPROVED    = "Approved"
    IS_SHOPPING = "Is shopping"
    CANCELLED   = "Cancelled"
    ORDERED     = "Ordered"
    DONE        = "Done"
    REFUNDED    = "Refunded"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
    
    
class CsvLogStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In-progress"
    DONE = "Done"

    @classmethod
    def choices(cls):
        return tuple((i, i.value) for i in cls)


class CsvLogType(str, Enum):
    INSERT = "Insert Only"
    UPSERT = "Insert and Update"
    EXPORT = "Export"

    @classmethod
    def choices(cls):
        return tuple((i, i.value) for i in cls)