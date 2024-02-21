from typing import Annotated
from pydantic import BaseModel, StringConstraints
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
    phone_number = Column(String(10))
    linkedin = Column(String(100))

    courses = relationship("Course", backref="owner")


class ViewTeacher(BaseModel):
    username: Annotated[str, StringConstraints(pattern='^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,5}$')]
    first_name: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    last_name: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    courses: list[CourseCard]
    phone_number: Annotated[str, StringConstraints(pattern='^\w{10,10}$')]|None
    linkedin: Annotated[str, StringConstraints(pattern='^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?$')]|None


    @classmethod
    def create_view_teacher(cls,
                            username: Annotated[str, StringConstraints(pattern='^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,5}$')],
                            first_name: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                            last_name: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                            courses: list[CourseCard],
                            phone_number: Annotated[str, StringConstraints(pattern='^\w{8,10}$')]|None,
                            linkedin: Annotated[str, StringConstraints(pattern='^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?$')]|None):
        return cls(
            username=username,
            first_name=first_name,
            last_name=last_name,
            courses=courses,
            phone_number=phone_number,
            linkedin=linkedin
        )