from pydantic import BaseModel


class User(BaseModel):
    id: int
    phone_number: str
    is_owner: bool
