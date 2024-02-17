from fastapi import APIRouter, Header
from models.course import CreateCourse
from models.section import CreateSection
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

    course: database.Course = database.get_record(database.Course)
    session = database.Session()
    session.add(course)
    sections = course.sections
    session.close()

    return sections


@courses_router.get('', status_code=200)
def get_all_courses():
    return course_service.get_all_courses()
