import database
from models.authentication import RegisterData, LoginData


def login(data: LoginData, user_type: str):
    user_type: database.Teacher|database.Student = get_type(user_type)
    account: database.Teacher|database.Student = database.get_record(database.session, user_type, email=data.email)[0]

    if account and account.password == hash_password(data.password):
        return account


def register(data: RegisterData, user_type: str):
    user_type = get_type(user_type)

    data.password = hash_password(data.password)

    database.add_record(database.session, user_type, email=data.email, password=data.password, first_name=data.first_name, last_name=data.last_name)


def user_exists(email):
    if database.get_record(database.session, database.Student, email=email):
        return True
    if database.get_record(database.session, database.Teacher, email=email):
        return True
    return False


def hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def get_type(user_type: str):
    if user_type=='teacher': user_type = database.Teacher
    if user_type=='student': user_type = database.Student
    return user_type