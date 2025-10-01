from enum import StrEnum


class UnsetType:
    def __repr__(self):
        return "<UNSET>"


UNSET = UnsetType()


class AccountStringFormat(StrEnum):
    DEFAULT = "DEFAULT"
    IAM_MOB = "IAM_MOB"
