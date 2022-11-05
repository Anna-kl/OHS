from enum import Enum


class ClassifierEnum(Enum):
    Av_amID = 1
    MfId = 2
    TipMf = 3
    PositionMUAlt = 4
    # "Наименования штатов и структурных подразделений"
    NameMU = 5
    # Идентификатор воинского формирования(1 уровень)
    VidMf_01 = 6
    VidMf_02 = 7
    VidMf_03 = 8
    CombatArm = 9
    # Классификатор - "Рода войск"
    Tk_kfor = 10
