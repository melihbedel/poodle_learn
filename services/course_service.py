from models.course import CourseCard, CreateCourse, Course, ViewCourse, CourseTag, EditCourse, EditInfo, EditTags
from models.section import SectionCard
from models.teacher import Teacher
from models.student import Student, StudentSubscription
from models.tag import Tag
import database

#Course

def get_all_courses():
    courses = database.get_record(Course)

    return form_course_cards(courses)


def create_course(owner_id: int, course: CreateCourse):
    new_course: Course = database.add_record(Course, owner_id=owner_id, title=course.title, description=course.description, objectives=course.objectives, private=course.private)

    for tag in course.tags:
        session = database.Session()
        new_tag: Tag = create_tag(tag)
        session.add(new_tag)
        session.add(new_course)
        add_tag(new_course.id, new_tag.id)
        session.close()
    
    return get_course_by_id(new_course.id)


def get_course_by_id(id: int):
    course: Course = database.get_record(Course, id=id)

    session = database.Session()
    session.add(course)

    course_view = ViewCourse.create_course(course.id,
                                           course.title,
                                           course.description,
                                           course.objectives,
                                           [tag.tag for tag in course.tags],
                                           [SectionCard.create_section_card(section.id, section.title, section.description) for section in course.sections]
)
    
    session.close()
    return course_view


def edit_course(update_info: EditCourse, course_id: int):

    info: dict = EditInfo.create_edit_info(update_info.title, update_info.description, update_info.objectives, update_info.private).model_dump(exclude_none=True)
    tags: dict = EditTags.create_edit_tags(update_info.add_tag, update_info.remove_tag).model_dump(exclude_none=True)

    if info:
        session = database.Session()
        session.execute(database.update(Course).where(Course.id==course_id).values(**info))
        session.commit()
        session.close()

    if tags:
        if 'add_tag' in tags:
            tag_list = tags['add_tag']
            for tag in tag_list:
                new_tag = create_tag(tag)
                add_tag(course_id, new_tag.id)
        if 'remove_tag' in tags:
            for tag in tags['remove_tag']:
                remove_tag(course_id, tag_id_by_tag_name(tag))

    return get_course_by_id(course_id)


def get_courses_by_name(name: str):
    session = database.Session()
    courses: list[Course] = session.query(Course).filter(Course.title.like(f'%{name}%')).all()
    session.close()

    course_cards = form_course_cards(courses)

    return course_cards


def get_courses_by_tag(tag: str):
    session = database.Session()

    tags: list[Tag] = session.query(Tag).filter(Tag.tag.like(f'%{tag}%')).all()

    courses: list[Course] = []

    for tag in tags:
        course_tags: list[CourseTag] = session.query(CourseTag).filter_by(tag_id=tag.id).all()
        for course_tag in course_tags:
            courses.append(session.query(Course).filter_by(id=course_tag.course_id).first())

    session.close()

    course_cards = form_course_cards(courses)

    return course_cards



#Tag

def create_tag(tag: str):
    tag = tag.lower()
    if tag_exists(tag):
        return database.get_record(Tag, tag=tag)
    return database.add_record(Tag, tag=tag)
    

def add_tag(course_id: int, tag_id: int):
    session = database.Session()
    tag = session.query(CourseTag).filter_by(course_id=course_id, tag_id=tag_id).first()
    tag_name = session.query(Tag).filter_by(id=tag_id).first()
    session.close()
    if tag:
        return f'{tag_name.tag} tag is already assigned.'

    database.add_record(CourseTag, course_id=course_id, tag_id=tag_id)


def remove_tag(course_id: int, tag_id: int):
    session = database.Session()

    tag = session.query(CourseTag).filter_by(course_id=course_id, tag_id=tag_id).first()
    tag_object = session.query(Tag).filter_by(id=tag_id).first()

    if not tag:
        return f'The tag {tag_object.tag} which you want to remove already does not exist.'

    session.delete(tag)
    session.commit()
    session.close()

    check = database.get_record(CourseTag, tag_id=tag_id)
    if not check:
        session = database.Session()
        session.delete(session.query(Tag).filter_by(id=tag_id).first())
        session.commit()
        session.close()


#Utility

def form_course_cards(courses: list[Course]) -> list[CourseCard]:
    course_cards=[]

    if not courses:
        return []
    
    session = database.Session()

    if not isinstance(courses, list):
        session.add(courses)
        course_cards.append(CourseCard.create_card(courses.id, courses.title, courses.description, [tag.tag for tag in courses.tags]))
    else:
        for course in courses:
            session.add(course)
            course_cards.append(CourseCard.create_card(course.id, course.title, course.description, [tag.tag for tag in course.tags]))
    
    session.close()

    return course_cards


def tag_id_by_tag_name(tag_name):
    session = database.Session()

    tag: Tag = session.query(Tag).filter_by(tag=tag_name).first()
    tag_id = tag.id

    session.close()
    return tag_id


#Chekcs

def is_owner(course_id: int, account: Teacher):
    session = database.Session()
    session.add(account)
    course: Course = session.query(Course).filter_by(id=course_id).first()
    course_owner_id = course.owner_id
    account_id = account.id
    session.close()

    if course_owner_id == account_id:
        return True
    return False


def is_private(course_id: int):
    session = database.Session()
    course: Course = session.query(Course).filter_by(id=course_id).first()
    private = course.private
    session.close()

    if private:
        return True
    return False


def is_subscribed(course_id: int, account: Student|Teacher):
    if type(account) == Student:
        session = database.Session()
        session.add(account)
        subscription: StudentSubscription = session.query(StudentSubscription).filter_by(student_id=account.id, course_id=course_id).first()
        session.close()

        if subscription:
            return True
        return False


def tag_exists(tag: str):
    tag = tag.lower()
    if database.get_record(Tag, tag=tag):
        return True
    return False


def course_exists(course_id):
    session = database.Session()
    course: Course = session.query(Course).filter_by(id=course_id).first()
    session.close()
    if course:
        return True
    return False

