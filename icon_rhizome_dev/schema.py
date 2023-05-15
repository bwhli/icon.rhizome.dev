from piccolo.columns import ForeignKey, Integer, Varchar
from piccolo.table import Table


class Irc2Token(Table):
    name: Varchar()
    symbol: Varchar()
    decimals: Integer()
    contract: Varchar(length=42)
