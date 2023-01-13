from decimal import Decimal

from icon_rhizome_dev.constants import EXA


class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def int_to_string(
        value: int,
        decimals: int = 4,
        exa: int = EXA,
    ):
        value_decimal = Decimal(value) / Decimal(10**exa)
        value_str = f"{value_decimal:,.{decimals}f}"
        return value_str

    @staticmethod
    def hex_to_int(value: str):
        value_int = int(value, 16)
        return value_int

    @staticmethod
    def fmt(value: float | int) -> str:
        value_str = f"{value:,.4f}".rstrip("0")
        return value_str
