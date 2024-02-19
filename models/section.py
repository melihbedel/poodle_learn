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
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]]
    content: str
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]


class ViewSection(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]]
    content: str
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]

    @classmethod
    def create_section(cls,
                       id: int,
                       title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                       description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]],
                       content: str,
                       link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]):
        return cls(
            id=id,
            title=title,
            description=description,
            content=content,
            link=link
        )
    

class SectionCard(BaseModel):
    id: int
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]]

    @classmethod
    def create_section_card(cls,
                            id: int,
                            title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')],
                            description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]]):
        return cls(
            id=id,
            title=title,
            description=description
        )


class EditSection(BaseModel):
    title: Annotated[str, StringConstraints(pattern='^\w{2,45}$')]
    description: Optional[Annotated[str, StringConstraints(pattern='^\w{5,200}$')]]
    content: str
    link: Optional[Annotated[str, StringConstraints(pattern='^https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^/\s]*)*$')]]