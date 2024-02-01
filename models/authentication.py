from pydantic import BaseModel

class LoginData(BaseModel):
    email: str
    password: str

class RegisterData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str