from pydantic import BaseModel

class SignupModel(BaseModel):
    name: str
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
