from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(45), nullable=False)
    description = Column(String(45))
    content = Column(String(500), nullable=False)


class CreateSection(BaseModel):
    title: str
    description: str|None
    content: str


class ViewSection(BaseModel):
    id: int
    title: str
    description: str|None
    content: str

    @classmethod
    def create_section(cls, id: int, title: str, description: str, content: str):
        return cls(
            id=id,
            title=title,
            description=description,
            content=content
        )