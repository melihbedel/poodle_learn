from database import Teacher, Student
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_jwt_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_payload(user: Teacher|Student):
    result = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    return result