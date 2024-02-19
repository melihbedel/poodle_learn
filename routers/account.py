from fastapi import APIRouter, Header, HTTPException
from services.authenticaion import token_service
from services import teacher_service
from services import student_service
from models.authentication import EditAccount
from models.course import EditCourse
from models import teacher
from models import student


account_router = APIRouter(prefix='/account', tags=['Account',])

@account_router.get('', status_code=200)
def view_profile(
    x_token = Header(default=None)
):

    account = token_service.check_token(x_token)

    if type(account) == teacher.Teacher:
        return teacher_service.profile(account)


    elif type(account) == student.Student:
        return student_service.profile(account)


@account_router.put('', status_code=200)
def update_profile(
    update_info: EditAccount|EditCourse,
    x_token = Header(default=None)
):
    
    account = token_service.check_token(x_token)

    if type(account) == teacher.Teacher:
        return teacher_service.edit_teacher(update_info, account)

    if type(account) == student.Student:
        return student_service.edit_student(update_info, account)