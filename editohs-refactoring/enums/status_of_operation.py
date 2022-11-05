from enum import Enum


class StatusEvent(Enum):
    CREATE = 1
    CLOSE = 2
    ERROR = 3
    CORRUPT = 4
    DEFAULT = 5
