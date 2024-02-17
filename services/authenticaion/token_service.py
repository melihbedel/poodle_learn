from fastapi import HTTPException
from models.teacher import Teacher
from models.student import Student
from services.authenticaion import authentication_service
import database
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_jwt_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_payload(user: Teacher|Student, type: str):
    result = {
        'email': user.email,
        'type': type
    }
    return result

def check_token(token: str) -> Teacher|Student|None:
    try:
        payload = decode_jwt_token(token)
        return database.get_record(authentication_service.get_type(payload['type']), email=payload['email'])
    except:
        raise HTTPException(status_code=401, detail='Invalid user.')