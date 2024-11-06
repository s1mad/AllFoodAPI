from pydantic import BaseModel


class UserCreate(BaseModel):
    phone_number: str
    password: str


class UserResponse(BaseModel):
    id: int
    phone_number: str
    is_owner: bool

    class Config:
        from_attributes = True
