from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.course import CourseCard
from database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)

    courses = relationship("Course", backref="owner")


class ViewTeacher(BaseModel):
    username: str
    first_name: str
    last_name: str
    courses: list[CourseCard]

    @classmethod
    def create_view_teacher(cls, username: str, first_name: str, last_name: str, courses: list[CourseCard]):
        return cls(
            username=username,
            first_name=first_name,
            last_name=last_name,
            courses=courses
        )
    
class EditTeacher(BaseModel):
    password: str|None = None
    first_name: str|None = None
    last_name: str|None = None