from typing import Annotated
from pydantic import BaseModel, StringConstraints


class LoginData(BaseModel):
    email: Annotated[str, StringConstraints(pattern='^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,5}$')]
    password: Annotated[str, StringConstraints(pattern='^.{8,45}$')]


class RegisterData(BaseModel):
    email: Annotated[str, StringConstraints(pattern='^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,5}$')]
    password: Annotated[str, StringConstraints(pattern='^.{8,45}$')]
    first_name: Annotated[str, StringConstraints(pattern='^[a-zA-Z]{2,45}$')]|None = None
    last_name: Annotated[str, StringConstraints(pattern='^[a-zA-Z]{2,45}$')]|None = None


class EditAccount(BaseModel):
    password: Annotated[str, StringConstraints(pattern='^.{8,45}$')]
    first_name: Annotated[str, StringConstraints(pattern='^[a-zA-Z]{2,45}$')]|None = None
    last_name: Annotated[str, StringConstraints(pattern='^[a-zA-Z]{2,45}$')]|None = None
    phone_number: Annotated[str, StringConstraints(pattern='^\d{10}$')]|None = None
    linkedin: Annotated[str, StringConstraints(pattern='^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?$')]|None = None