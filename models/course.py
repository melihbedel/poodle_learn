from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.section import Section


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    title = Column(String(45), unique=True, nullable=False)
    description = Column(String(45), nullable=False)
    objectives = Column(String(45), nullable=False)
    private = Column(Boolean, nullable=False)

    tags = relationship("Tag", secondary="course_has_tags", back_populates="courses")
    sections = relationship("Section", backref="course")
    subscriptions = relationship("Student", secondary="student_has_subscriptions", back_populates='subscriptions')


class CourseTag(Base):
    __tablename__ = "course_has_tags"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class CreateCourse(BaseModel):
    title: str
    description: str
    objectives: str
    private: bool
    tags: list[str]


class ViewCourse(BaseModel):
    id: int
    title: str
    description: str
    objectives: str
    tags: list[str]
    sections: list
    
    @classmethod
    def create_course(cls, id: int,title: str, description: str, objectives: str, tags: list[str], sections: list):
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
    title: str
    description: str
    tags: list[str]

    @classmethod
    def create_card(cls, id: int, title: str, description: str, tags: list[str]):
        return cls(
            id=id,
            title=title,
            description=description,
            tags=tags
        )