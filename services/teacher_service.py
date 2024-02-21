from models.teacher import Teacher, ViewTeacher
from models.course import CourseCard, Course
from models.authentication import EditAccount
from services import course_service
from services.authenticaion import authentication_service
import database


def profile(account: Teacher):
    session = database.Session()
    session.add(account)

    profile: ViewTeacher = ViewTeacher.create_view_teacher(account.email, account.first_name, account.last_name, get_teacher_course_cards(account.id), account.phone_number, account.linkedin)
    final = profile.model_dump(exclude_none=True)
    session.close()

    return final


def get_teacher_course_cards(teacher_id: int) -> list[CourseCard]:
    courses: list[Course] = database.get_record(Course, owner_id=teacher_id)

    course_cards: list[CourseCard] = course_service.form_course_cards(courses)

    return course_cards


def edit_teacher(update_info: EditAccount, account: Teacher):

    update_info_dict = update_info.model_dump(exclude_unset=True)

    update = {}

    for key, value in update_info_dict.items():
        update[key] = value

    if 'password' in update:
        update['password'] = authentication_service.hash_password(update['password'])


    session = database.Session()
    session.add(account)
    session.execute(database.update(Teacher).where(Teacher.id==account.id).values(**update))
    session.commit()
    session.close()

    return {f"'{attr}' is set to '{value}'" for attr, value in update_info_dict.items()}    