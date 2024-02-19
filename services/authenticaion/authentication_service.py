from fastapi import HTTPException
from models.student import Student
from models.teacher import Teacher
import database
from models.authentication import RegisterData, LoginData


def login(data: LoginData, user_type: str):
    user_type = get_type(user_type)
    account: Teacher|Student = database.get_record(user_type, email=data.email)

    if account and account.password == hash_password(data.password):
        return account
    raise HTTPException(status_code=400, detail='Invalid login data.')


def register(data: RegisterData, user_type: str):
    user_type = get_type(user_type)

    data.password = hash_password(data.password)

    database.add_record(user_type, email=data.email, password=data.password, first_name=data.first_name, last_name=data.last_name)

    return f'{data.email} registered successfully.'


def user_exists(email: str):
    if database.get_record(Student, email=email):
        return True
    if database.get_record(Teacher, email=email):
        return True
    return False


def hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def get_type(user_type: str) -> Teacher|Student:
    if user_type=='teacher': user_type = Teacher
    if user_type=='student': user_type = Student
    return user_type