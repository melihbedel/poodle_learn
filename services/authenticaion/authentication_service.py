import database
from models.user_data import UserData

def login(data: UserData, user_type: str):
    if user_type=='teacher': user_type = database.Teacher
    if user_type=='student': user_type = database.Student

    account = None

    if database.get_records(database.session, user_type, email=data.email)


def register(data: UserData, user_type: str):
    if user_type=='teacher': user_type = database.Teacher
    if user_type=='student': user_type = database.Student

    data.password = hash_password(data.password)

    database.add_record(database.session, user_type, email=data.email, password=data.password, first_name=data.first_name, last_name=data.last_name)


def user_exists(email):
    if database.get_records(database.session, database.Student, email=email):
        return True
    if database.get_records(database.session, database.Teacher, email=email):
        return True
    return False


def hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()
