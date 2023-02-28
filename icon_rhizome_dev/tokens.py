from pydantic import BaseModel


class Tokens:
    class Irc2Token(BaseModel):
        contract: str
        symbol: str
        decimals: int

    TOKENS = {
        "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": Irc2Token(
            contract="cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
            symbol="BALN",
            decimals=18,
        ),
        "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": Irc2Token(
            contract="cx88fd7df7ddff82f7cc735c871dc519838cb235bb",
            symbol="bnUSD",
            decimals=18,
        ),
        "cxb49d82c46be6b61cab62aaf9824b597c6cf8a25d": Irc2Token(
            contract="cxb49d82c46be6b61cab62aaf9824b597c6cf8a25d",
            symbol="BUSD",
            decimals=18,
        ),
        "cxae3034235540b924dfcc1b45836c293dcc82bfb7": Irc2Token(
            contract="cxae3034235540b924dfcc1b45836c293dcc82bfb7",
            symbol="IUSDC",
            decimals=6,
        ),
        "cxae3034235540b924dfcc1b45836c293dcc82bfb7": Irc2Token(
            contract="cxae3034235540b924dfcc1b45836c293dcc82bfb7",
            symbol="IUSDC",
            decimals=6,
        ),
        "cx2609b924e33ef00b648a409245c7ea394c467824": Irc2Token(
            contract="cx2609b924e33ef00b648a409245c7ea394c467824",
            symbol="sICX",
            decimals=18,
        ),
        "cxbb2871f468a3008f80b08fdde5b8b951583acf06": Irc2Token(
            contract="cxbb2871f468a3008f80b08fdde5b8b951583acf06",
            symbol="USDS",
            decimals=18,
        ),
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def get_decimals_by_contract(cls, contract: str) -> int:
        return cls.TOKENS[contract].decimals

    @classmethod
    def get_symbol_by_contract(cls, contract: str) -> str:
        return cls.TOKENS[contract].symbol
