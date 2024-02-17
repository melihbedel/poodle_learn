from models.teacher import Teacher, ViewTeacher, EditTeacher
from models.course import CourseCard, Course
from services import course_service
from services.authenticaion import authentication_service
import database


def profile(account: Teacher):
    session = database.Session()
    session.add(account)

    profile = ViewTeacher.create_view_teacher(account.email, account.first_name, account.last_name, get_teacher_course_cards(account.id))

    session.close()

    return profile


def get_teacher_course_cards(teacher_id: int) -> list[CourseCard]:
    courses: list[Course] = database.get_record(Course, owner_id=teacher_id)

    course_cards: list[CourseCard] = course_service.form_course_cards(courses)

    return course_cards


def edit_teacher(updated_info: EditTeacher, account: Teacher):
    original_update = EditTeacher(password=updated_info.password, first_name=updated_info.first_name, last_name=updated_info.last_name)

    if updated_info.password:
        updated_info.password = authentication_service.hash_password(updated_info.password)

    updated_info_dict = updated_info.model_dump(exclude_unset=True)

    session = database.Session()
    session.add(account)

    session.execute(database.update(Teacher).where(Teacher.id==account.id).values(**updated_info_dict))

    session.close()

    original_update_dict = original_update.model_dump(exclude_unset=True)

    return {f"'{attr}' is set to '{value}'" for attr, value in original_update_dict.items()}