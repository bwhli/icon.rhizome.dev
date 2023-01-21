from pydantic import BaseModel


class BalancedPool:
    pool_id: int


class BalancedLoanAssets:
    bnUSD: int
    sICX: int


class BalancedLoanStanding:
    collateral: int
    ratio: int
    standing: str
    total_debt: int


class BalancedLoanStandings:
    BTCB: BalancedLoanStanding
    ETH: BalancedLoanStanding
    sICX: BalancedLoanStanding


class BalancedLoan:
    address: str
    assets: BalancedLoanAssets
    collateral: int
    created: int
    holdings: dict
    pos_id: int
    ratio: int
    standing: str
    standings: BalancedLoanStandings
    total_debt: int
