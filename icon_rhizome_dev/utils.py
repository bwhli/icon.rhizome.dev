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
