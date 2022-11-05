from enum import Enum


class StatusOperation(Enum):
    CREATE = 1
    COMMIT = 2
    ERROR = 3
    REJECT = 4
