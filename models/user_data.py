from pydantic import BaseModel

class UserData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str