from models.section import CreateSection, Section, ViewSection, EditSection
import database


def create_section(course_id: int, section: CreateSection):
    section = database.add_record(Section, course_id=course_id, title=section.title, description=section.description, content=section.content, link=section.link)
    session = database.Session()
    session.add(section)
    section_id = section.id
    session.close()
    return get_section_by_id(section_id)


def get_section_by_id(section_id):
    session = database.Session()
    section: Section = session.query(Section).filter_by(id=section_id).first()
    section_view: ViewSection = ViewSection.create_section(id=section.id, title=section.title, description=section.description, content=section.content, link=section.link)
    section_dict = section_view.model_dump(exclude_none=True)
    session.close()

    return section_dict


def edit_section(update_info: EditSection, section_id: int):

    edit: dict = update_info.model_dump(exclude_none=True, exclude_unset=True)

    if edit:
        session = database.Session()
        session.execute(database.update(Section).where(Section.id==section_id).values(**edit))
        session.commit()
        session.close()

    return get_section_by_id(section_id)


def section_exists(course_id, section_id):
    session = database.Session()
    section: Section = session.query(Section).filter_by(id=section_id, course_id=course_id).first()
    session.close()
    if section:
        return True
    return False