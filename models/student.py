from pydantic import BaseModel
from models.course import CourseCard
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)

    subscriptions = relationship("Course", secondary="student_has_subscriptions", back_populates='subscriptions')


class StudentSubscription(Base):
    __tablename__ = "student_has_subscriptions"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)



class ViewStudent(BaseModel):
    username: str
    first_name: str
    last_name: str
    subscriptions: list[CourseCard]

    @classmethod
    def create_view_student(cls, username: str, first_name: str, last_name: str, subscriptions: list[CourseCard]):
        return cls(
            username=username,
            first_name=first_name,
            last_name=last_name,
            subscriptions=subscriptions
        )