from typing import Union, List
import database
from models.courses import CourseCard, CreateCourse, CreateSection


def create_course(owner_id: int, course: CreateCourse):
    new_course: database.Course = database.add_record(database.Course, owner_id=owner_id, title=course.title, description=course.description, objectives=course.objectives, private=course.private)

    for tag in course.tags:
        new_tag: database.Tag = create_tag(tag)
        session = database.Session()
        session.add(new_course)
        session.add(new_tag)
        database.add_record(database.CourseTag, course_id=new_course.id, tag_id=new_tag.id)
        session.close()

        session = database.Session()
        session.add(new_course)
        course_id = new_course.id
        session.close()
    
    return get_course_by_id(course_id)


def get_course_by_id(id):
    course = database.get_record(database.Course, id=id)
    return course


def create_section(course_id: int, section: CreateSection):
    database.add_record(database.Section, course_id=course_id, title=section.title, description=section.description, content=section.content)

    







def create_tag(tag: str):
    tag = tag.lower()
    if tag_exists(tag):
        return database.get_record(database.Tag, tag=tag)
    return database.add_record(database.Tag, tag=tag)
    


def tag_exists(tag: str):
    tag = tag.lower()
    if database.get_record(database.Tag, tag=tag):
        return True
    return False





def get_all_courses():
    courses: list[database.Course]|database.Course = database.get_record(database.Course)
    
    course_cards = []

    for course in courses:
        tags = get_course_tags(course.id)
        tags_list = [tag.tag for tag in tags]
        course_cards.append(CourseCard.create_card(course.title, course.description, tags_list))

    return course_cards


def get_course_tags(course_id) -> list[database.Tag]:
    course_tag_relations = database.get_record(database.CourseTag, course_id=course_id)
    tags = []
    if not isinstance(course_tag_relations, list):
        tags.append(database.get_record(database.Tag, id=course_tag_relations.tag_id))
        return tags
    for relation in course_tag_relations:
        tags.append(database.get_record(database.Tag, id=relation.tag_id))
    return tags


# public_courses = database.get_record(database.session, database.Course, private=0)

# public_course_cards = []

# for course in public_courses:
#     public_course_cards.append(CourseCard(title=course.title, description=course.description, tags=[tag for tag in course.tags]))
