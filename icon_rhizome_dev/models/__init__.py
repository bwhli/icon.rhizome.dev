from pydantic import BaseModel


class Result(BaseModel):
    default: int | float
    string: str = None
