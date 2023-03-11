from datetime import datetime

from pydantic import BaseModel

from icon_rhizome_dev.icx import Icx


class BalancedDividendClaim(BaseModel):
    contract: str
    symbol: str
    amount: float
    transaction_hash: str
    block_number: int
    timestamp: datetime


class Balanced(Icx):

    CONTRACT_BALANCED_DEX = "cxa0af3165c08318e988cb30993b3048335b94af6c"
    CONTRACT_BALANCED_DIVIDENDS = "cx203d9cd2a669be67177e997b8948ce2c35caffae"
    CONTRACT_BALANCED_LOANS = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    CONTRACT_BALANCED_ORACLE = "cx133c6015bb29f692b12e71c1792fddf8f7014652"
    CONTRACT_BALANCED_PEG_STABILITY = "cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6"

    def __init__(self) -> None:
        pass
