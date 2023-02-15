from pydantic import BaseModel


class Tokens:
    class Irc2Token(BaseModel):
        contract: str
        symbol: str
        decimals: int

    TOKENS = {
        "cxae3034235540b924dfcc1b45836c293dcc82bfb7": Irc2Token(
            contract="cxae3034235540b924dfcc1b45836c293dcc82bfb7",
            symbol="IUSDC",
            decimals=6,
        ),
        "cxbb2871f468a3008f80b08fdde5b8b951583acf06": Irc2Token(
            contract="cxbb2871f468a3008f80b08fdde5b8b951583acf06",
            symbol="USDS",
            decimals=18,
        ),
        "cxb49d82c46be6b61cab62aaf9824b597c6cf8a25d": Irc2Token(
            contract="cxb49d82c46be6b61cab62aaf9824b597c6cf8a25d",
            symbol="BUSD",
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
