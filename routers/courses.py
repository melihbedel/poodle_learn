from fastapi import APIRouter, Header, Query, HTTPException
from models.student import Student
from models.course import CreateCourse, Course, EditCourse
from models.section import CreateSection
from models.teacher import Teacher
from services import student_service
from services import course_service
from services import section_service
from services.authenticaion import token_service

courses_router = APIRouter(prefix='/courses', tags=['Courses'])


# Course

@courses_router.get('', status_code=200)
def get_all_courses(
    name: str = Query(None),
    tag: str = Query(None)
):
    if name and tag:
        raise HTTPException(status_code=403, detail='You cannot search for a name and tag simultaneously.')
    if name:
        return course_service.get_courses_by_name(name)
    if tag:
        return course_service.get_courses_by_tag(tag)
    
    return course_service.get_all_courses()



@courses_router.post('', status_code=200)
def post_course(
    course: CreateCourse,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    if type(user) != Teacher:
        raise HTTPException(status_code=403, detail='Only teachers can create courses.')
    
    return course_service.create_course(owner_id=user.id, course=course)



@courses_router.get('/{id}', status_code=200)
def view_course(
    id: int,
    x_token: str = Header(default=None)
):
    
    user = token_service.check_token(x_token)
    if not course_service.course_exists(id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')
    if course_service.is_private(id):
        if not course_service.is_subscribed(id, user):
            raise HTTPException(status_code=401, detail='You cannot access private courses without subscribing.')


    return course_service.get_course_by_id(id)



@courses_router.put('/{id}', status_code=200)
def edit_course(
    id: int,
    edit: EditCourse,
    x_token: str = Header(default=None)
):

    user = token_service.check_token(x_token)
    if not course_service.course_exists(id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')
    if not course_service.is_owner(id, user):
        raise HTTPException(status_code=403, detail='You must be the owner of the course to edit.')

    return course_service.edit_course(edit, id)



# Section

@courses_router.post('/{id}', status_code=200)
def add_section(
    id: int,
    section: CreateSection,
    x_token: str = Header(default=None)
):
    
    user = token_service.check_token(x_token)
    if not course_service.course_exists(id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')
    if not course_service.is_owner(id, user):
        raise HTTPException(status_code=403, detail='You must be the owner of the course to edit.')

    return section_service.create_section(course_id=id, section=section)


@courses_router.get('/{course_id}/{section_id}', status_code=200)
def view_section(
    course_id: int,
    section_id: int,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    if not course_service.course_exists(course_id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')
    if course_service.is_private(course_id):
        if not course_service.is_subscribed(course_id, user):
            raise HTTPException(status_code=401, detail='You cannot access private courses without subscribing.')
    if not section_service.section_exists(course_id, section_id):
        raise HTTPException(status_code=404, detail=f'Section ID:{section_id} does not exist in Course ID:{course_id}')
        
    return section_service.get_section_by_id(section_id)


@courses_router.put('/{course_id}/{section_id}', status_code=200)
def edit_section(
    course_id: int,
    section_id: int,
    edit: EditCourse,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    if not course_service.course_exists(course_id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')
    if not course_service.is_owner(course_id, user):
        raise HTTPException(status_code=403, detail='You must be the owner of the course to edit.')
    if not section_service.section_exists(course_id, section_id):
        raise HTTPException(status_code=404, detail=f'Section:{section_id} does not exist in Course:{course_id}.')
    
    section_service.edit_section(edit, section_id)

    return section_service.get_section_by_id(section_id)



# Subscription

@courses_router.post('/{id}/subscribe', status_code=201)
def subscribe(
    id: int,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    if not course_service.course_exists(id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')

    if type(user) != Student:
        raise HTTPException(status_code=401, detail='You have to be a Student in order to subscribe to courses.')
    
    return student_service.subscribe(id, user)
    


@courses_router.post('/{id}/unsubscribe', status_code=201)
def unsubscribe(
    id: int,
    x_token: str = Header(default=None)
):
    user = token_service.check_token(x_token)
    if not course_service.course_exists(id):
        raise HTTPException(status_code=404, detail=f'Course with ID:{id} does not exist.')

    if type(user) != Student:
        raise HTTPException(status_code=401, detail='You have to be a Student in order to unsubscribe from courses.')
    
    return student_service.unsubscribe(id, user)