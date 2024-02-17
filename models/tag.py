from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(45), nullable=False)

    courses = relationship("Course", secondary="course_has_tags", back_populates="tags")