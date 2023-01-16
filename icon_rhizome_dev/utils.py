from decimal import Decimal

from rich import inspect
from yarl import URL

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
        return int(value, 16)

    @staticmethod
    def int_to_hex(value: int):
        return hex(value)

    @staticmethod
    def fmt(value: float | int) -> str:
        if isinstance(value, int):
            return f"{value:,}"
        else:
            value_str = f"{value:,.4f}".rstrip("0")
            return value_str

    @staticmethod
    def format_number(value: float | int, decimal_places: int = 4) -> str:

        if float(value) == int(value):
            value = int(value)

        if decimal_places == 0:
            value = int(value)

        if isinstance(value, int):
            return f"{value:,}"
        else:
            value_str = f"{value:,.{decimal_places}f}".rstrip("0")
            return value_str

    @staticmethod
    def format_percentage(value: float) -> str:
        if int(value) == float(value):
            return f"{int(value)}%"
        return f"{value:.2%}"
