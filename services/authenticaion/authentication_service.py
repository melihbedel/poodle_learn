import database
from models.user_data import UserData

def register(data: UserData, user_type: str):

    if user_type=='teacher': user_type = database.Teacher
    if user_type=='student': user_type = database.Student

    if user_exists(data, user_type):
        raise f'User with this email already exists'

    database.add_record(database.session, user_type, email=data.email, password=data.password, first_name=data.first_name, last_name=data.last_name)



def user_exists(data: UserData, user_type: database.Teacher|database.Student):
    if database.get_records(database.session, user_type, email=data.email):
        return True
    return False


