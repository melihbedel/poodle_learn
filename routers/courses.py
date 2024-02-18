from fastapi import APIRouter, Header, Query, HTTPException
from models.student import Student
from models.course import CreateCourse, Course
from models.section import CreateSection
from services import student_service
from services import course_service
from services.authenticaion import token_service
import database

courses_router = APIRouter(prefix='/courses', tags=['Courses'])



@courses_router.post('', status_code=200)
def post_course(
    course: CreateCourse,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    return course_service.create_course(owner_id=user.id, course=course)




@courses_router.post('/{id}', status_code=200)
def add_section(
    id: int,
    section: CreateSection,
    x_token: str = Header(default=None)
):
    course_service.create_section(course_id=id, section=section)

    return course_service.get_course_by_id(id)



@courses_router.get('', status_code=200)
def get_all_courses(
    x_token: str = Header(default=None)
):
    return course_service.get_all_courses()




@courses_router.get('/{id}', status_code=200)
def view_course(
    id: int

):
    return course_service.get_course_by_id(id)





@courses_router.post('/{id}/subscribe', status_code=200)
def subscribe(
    id: int,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)

    if type(user) != Student:
        raise HTTPException(status_code=401, detail='You have to be a Student in order to subscribe to courses.')
    
    return student_service.subscribe(id, user)
    




@courses_router.post('/{id}/unsubscribe', status_code=200)
def unsubscribe(
    id: int,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)

    if type(user) != Student:
        raise HTTPException(status_code=401, detail='You have to be a Student in order to unsubscribe from courses.')
    
    return student_service.unsubscribe(id, user)