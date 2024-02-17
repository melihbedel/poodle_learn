from models.course import CourseCard, CreateCourse, Course, ViewCourse, CourseTag
from models.section import CreateSection, Section
from models.tag import Tag
import database


def create_course(owner_id: int, course: CreateCourse):
    new_course: Course = database.add_record(Course, owner_id=owner_id, title=course.title, description=course.description, objectives=course.objectives, private=course.private)

    for tag in course.tags:
        new_tag: Tag = create_tag(tag)
        session = database.Session()
        session.add(new_course)
        session.add(new_tag)
        database.add_record(CourseTag, course_id=new_course.id, tag_id=new_tag.id)
        session.close()

        session = database.Session()
        session.add(new_course)
        course_id = new_course.id
        session.close()
    
    return get_course_by_id(course_id)


def get_course_by_id(id):
    course: Course = database.get_record(Course, id=id)
    session = database.Session()
    session.add(course)
    course_view = ViewCourse.create_course(course.id, course.title, course.description, course.objectives, [tag.tag for tag in course.tags], course.sections)
    session.close()
    return course_view


def create_section(course_id: int, section: CreateSection):
    database.add_record(Section, course_id=course_id, title=section.title, description=section.description, content=section.content)


def create_tag(tag: str):
    tag = tag.lower()
    if tag_exists(tag):
        return database.get_record(Tag, tag=tag)
    return database.add_record(Tag, tag=tag)
    


def tag_exists(tag: str):
    tag = tag.lower()
    if database.get_record(Tag, tag=tag):
        return True
    return False





def get_all_courses():
    courses = database.get_record(Course)

    return form_course_cards(courses)


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