from fastapi import APIRouter, Header
from models.courses import CreateCourse
from services import course_service
from services.authenticaion import token_service

courses_router = APIRouter(prefix='/courses', tags=['Courses'])

@courses_router.post('', status_code=200)
def post_course(
    course: CreateCourse,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    course_service.create_course(owner_id=user.id, course=course)
