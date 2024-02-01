from services.authenticaion.authentication_service import hash_password
import database
from models.authentication import LoginData
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_jwt_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_payload(user: database.Teacher|database.Student, type: str):
    result = {
        'email': user.email,
        'type': type
    }
    return result

def check_token(token: str):
    payload = decode_jwt_token(token)
    if payload:
        return database.get_record(database.session, payload['type'], email=payload['email'])[0]
    return False