from fastapi import HTTPException
from models.student import Student, ViewStudent, StudentSubscription
from models.course import CourseCard, Course
from models.authentication import EditAccount
from services import course_service
from services.authenticaion import authentication_service
import database


def profile(account: Student):
    session = database.Session()
    session.add(account)

    profile = ViewStudent.create_view_student(account.email, account.first_name, account.last_name, get_student_subscriptions(account.id))

    session.close()

    return profile


def get_student_subscriptions(student_id: int) -> list[str]:
    subscriptions: list[StudentSubscription]|StudentSubscription = database.get_record(StudentSubscription, student_id=student_id)
    
    session = database.Session()

    subscribed_courses: list[Course] = []

    if not subscriptions:
        return []
    if not isinstance(subscriptions, list):
        session.add(subscriptions)
        subscribed_courses.append(database.get_record(Course, id=subscriptions.course_id))
    else:
        for subscription in subscriptions:
            session.add(subscription)
            subscribed_courses.append(database.get_record(Course, id=subscription.course_id))

    course_cards: list[CourseCard] = course_service.form_course_cards(subscribed_courses)

    return course_cards


def edit_student(update_info: EditAccount, account: Student):

    update_info_dict = update_info.model_dump(exclude_unset=True)

    update = {}

    for key, value in update_info_dict.items():
        update[key] = value

    if 'password' in update:
        update['password'] = authentication_service.hash_password(update['password'])


    session = database.Session()
    session.add(account)
    session.execute(database.update(Student).where(Student.id==account.id).values(**update))
    session.commit()
    session.close()

    return {f"'{attr}' is set to '{value}'" for attr, value in update_info_dict.items()}



def subscribe(course_id: int, account: Student):

    if subscription_exists(account.id, course_id):
        raise HTTPException(status_code=403, detail='You are already subscribed to this course.')

    session = database.Session()
    session.add(account)
    database.add_record(StudentSubscription, student_id=account.id, course_id=course_id)
    session.commit()
    session.close()

    return profile(account)


def unsubscribe(course_id: int, account: Student):

    if not subscription_exists(account.id, course_id):
        raise HTTPException(status_code=403, detail='You are not subscribed to this course')

    session = database.Session()
    session.add(account)
    session.delete(session.query(StudentSubscription).filter_by(student_id=account.id, course_id=course_id).first())
    session.commit()
    session.close()

    return profile(account)


def subscription_exists(student_id, course_id):
    subscription: StudentSubscription = database.get_record(StudentSubscription, student_id=student_id, course_id=course_id)

    if subscription:
        return True
    return False