from pydantic import BaseModel


class CreateCourse(BaseModel):
    title: str
    description: str
    objectives: str
    private: bool
    tags: list[str]

class Course(BaseModel):
    title: str
    description: str
    objectives: str
    tags: list[str]
    sections: list[str]


class CreateSection(BaseModel):
    title: str
    description: str|None
    content: str

class Section(BaseModel):
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

class CourseCard(BaseModel):
    title: str
    description: str
    tags: list[str]

    @classmethod
    def create_card(cls, title: str, description: str, tags: list[str]):
        return cls(
            title=title,
            description=description,
            tags=tags
        )