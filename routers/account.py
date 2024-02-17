from fastapi import APIRouter, Header, HTTPException
from services.authenticaion import token_service
from services import teacher_service
from services import student_service
from models import teacher
from models import student
import database


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
    edited_teacher: teacher.EditTeacher,
    x_token = Header(default=None)
):
    
    account = token_service.check_token(x_token)

    if type(account) == teacher.Teacher:
        return teacher_service.edit_teacher(updated_info=edited_teacher, account=account)


    elif type(account) == student.Student:
        pass