from typing import Annotated
from pydantic import BaseModel, StringConstraints
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.section import Section


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    title = Column(String(45), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    objectives = Column(String(200), nullable=False)
    private = Column(Boolean, nullable=False)

    tags = relationship("Tag", secondary="course_has_tags", back_populates="courses")
    sections = relationship("Section", backref="course")
    subscriptions = relationship("Student", secondary="student_has_subscriptions", back_populates='subscriptions')


class CourseTag(Base):
    __tablename__ = "course_has_tags"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class CreateCourse(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]
    objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]
    private: bool
    tags: list[str]


class ViewCourse(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]
    objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]
    tags: list[Annotated[str, StringConstraints(pattern='^\w{2,45}$')]]
    sections: list
    
    @classmethod
    def create_course(cls,
                      id: int,
                      title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                      description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')],
                      objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')],
                      tags: list[Annotated[str, StringConstraints(pattern='^\w{2,45}$')]],
                      sections: list):
        return cls(
            id=id,
            title=title,
            description=description,
            objectives=objectives,
            tags=tags,
            sections=sections
        )


class CourseCard(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]
    tags: list[Annotated[str, StringConstraints(pattern='^\w{2,45}$')]]

    @classmethod
    def create_card(cls,
                    id: int,
                    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')],
                    tags: list[Annotated[str, StringConstraints(pattern='^\w{2,45}$')]]):
        return cls(
            id=id,
            title=title,
            description=description,
            tags=tags
        )


class EditCourse(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]|None = None
    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None = None
    objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None = None
    private: bool|None = None
    add_tag: list[str]|None = None
    remove_tag: list[str]|None = None


class EditInfo(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]|None = None
    description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None = None
    objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None = None
    private: bool|None = None

    @classmethod
    def create_edit_info(cls,
                         title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]|None,
                         description: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None,
                         objectives: Annotated[str, StringConstraints(pattern='^\w{5,200}$')]|None,
                         private: bool|None):
        return cls(
            title=title,
            description=description,
            objectives=objectives,
            private=private
        )


class EditTags(BaseModel):
    add_tag: list[str]|None = None
    remove_tag: list[str]|None = None

    @classmethod
    def create_edit_tags(cls,
                         add_tag: list[str]|None,
                         remove_tag: list[str]|None):
        return cls(
            add_tag=add_tag,
            remove_tag=remove_tag
        )