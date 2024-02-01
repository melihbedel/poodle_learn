import database
from models.courses import CourseCard, CreateCourse


def create_course(owner_id: int, course: CreateCourse):
    new_course: database.Course = database.add_record(database.session, database.Course, owner_id=owner_id, title=course.title, description=course.description, objectives=course.objectives, private=course.private)

    for tag in course.tags:
        if not tag_exists(tag):
            database.add_record(database.session, database.Tag, tag=tag)
        new_tag: database.Tag = database.get_record(database.session, database.Tag, tag=tag)[0]
        new_course.tags.append(new_tag)


def tag_exists(tag: str):
    if database.get_record(database.session, database.Tag, tag=tag):
        return True
    return False





# public_courses = database.get_record(database.session, database.Course, private=0)

# public_course_cards = []

# for course in public_courses:
#     public_course_cards.append(CourseCard(title=course.title, description=course.description, tags=[tag for tag in course.tags]))
