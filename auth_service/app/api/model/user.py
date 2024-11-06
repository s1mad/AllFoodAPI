from pydantic import BaseModel

class UserCreate(BaseModel):
    phone_number: str
    password: str
    is_owner: bool = False

class UserResponse(BaseModel):
    id: int
    phone_number: str
    is_owner: bool

    class Config:
        from_attributes = True
