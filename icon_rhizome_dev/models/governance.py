from pydantic import BaseModel

from icon_rhizome_dev.models import Result


class Validator(BaseModel):
    address: str
    api_endpoint: str = None
    bonded: int = None
    city: str
    country: str
    cps_governance: bool
    created_blocks: int = None
    reward_icx_daily: float = None
    reward_usd_daily: float = None
    reward_usd_monthly: float = None
    reward_usd_monthly: float = None
    delegated: float = None
    details: str
    email: str = None
    facebook: str = None
    github: str = None
    grade: str = None
    irep: int = None
    logo_256: str = None
    logo_512: str = None
    logo_1024: str = None
    logo_svg: str = None
    name: str
    node_address: str = None
    p2p_endpoint: str
    power: int = None
    productivity: float = None
    sponsored_cps_grants: int = None
    stake: int
    status: str = None
    telegram: str = None
    total_blocks: int = None
    twitter: str = None
    validated_blocks: int = None
    voted: int = None
    voting_power: int = None
    website: str = None
