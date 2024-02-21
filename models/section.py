from typing import Optional, Annotated
from pydantic import BaseModel, StringConstraints
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(45), nullable=False)
    description = Column(String(200))
    content = Column(String(500), nullable=False)
    link = Column(String(200))


class CreateSection(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^.{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None
    content: str
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]|None = None


class ViewSection(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^.{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None
    content: str
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]|None

    @classmethod
    def create_section(cls,
                       id: int,
                       title: Annotated[str, StringConstraints(pattern='^.{2,45}$')],
                       content: str,
                       description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None,
                       link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]|None = None):
        return cls(
            id=id,
            title=title,
            description=description,
            content=content,
            link=link
        )
    

class SectionCard(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^.{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None

    @classmethod
    def create_section_card(cls,
                            id: int,
                            title: Annotated[str, StringConstraints(pattern='^.{2,45}$')],
                            description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None):
        return cls(
            id=id,
            title=title,
            description=description
        )


class EditSection(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^.{2,45}$')]|None = None
    description: Optional[Annotated[str, StringConstraints(pattern='^.{5,200}$')]]|None = None
    content: str|None = None
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]|None = None