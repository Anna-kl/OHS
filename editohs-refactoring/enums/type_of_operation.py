from enum import Enum


class TypeOfOperation(Enum):
    ADD = 1
    DELETE = 2
    UPDATE = 3
    ADDRECORD = 4
    UPDATERECORD = 5
    DELETERECORD = 6
    SNAPSHOT = 7
    DEFAULT = 8