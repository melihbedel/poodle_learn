from pydantic import BaseModel


class LoginData(BaseModel):
    email: str
    password: str


class RegisterData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class EditAccount(BaseModel):
    password: str|None = None
    first_name: str|None = None
    last_name: str|None = None