from pydantic import BaseModel


class CreateCourse(BaseModel):
    title: str
    description: str
    objectives: str
    private: bool
    tags: list[str]


class CourseCard(BaseModel):
    title: str
    description: str
    tags: list[str]