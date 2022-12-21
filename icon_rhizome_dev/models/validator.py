from pydantic import BaseModel

from icon_rhizome_dev.models import Result


class Validator(BaseModel):
    address: str
    api_endpoint: str = None
    bonded: int = None
    city: str
    country: str
    cps_governance: bool
    created_block: int
    delegated: float
    details: str
    email: str
    facebook: str
    github: str
    grade: str
    irep: int
    logo_256: str
    name: str
    node_address: str
    p2p_endpoint: str
    power: int
    sponsored_cps_grants: int
    stake: int
    status: str
    telegram: str
    total_blocks: int
    twitter: str
    validated_blocks: int
    voted: int
    voting_power: int
    website: str
