from pydantic import BaseModel


class Result(BaseModel):
    default: int
    string: str
