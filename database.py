from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta


DATABASE_URL = 'mysql+pymysql://root:1234@127.0.0.1:3306/poodle_learn'
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    courses = relationship("Course", back_populates="owner")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    title = Column(String(45), nullable=False, unique=True)
    description = Column(String(45), nullable=False)
    objectives = Column(String(45), nullable=False)
    private = Column(Boolean, nullable=False)
    owner = relationship("Teacher", back_populates="courses")
    sections = relationship("Section", back_populates="course")


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(45), nullable=False)
    description = Column(String(45))
    content = Column(String(500), nullable=False)
    course = relationship("Course", back_populates="sections")


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)


class StudentSubscription(Base):
    __tablename__ = 'student_has_subscriptions'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    student = relationship("Student")
    course = relationship("Course")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String(45), nullable=False)


class CourseTag(Base):
    __tablename__ = 'course_has_tags'

    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    course = relationship("Course", backref="course_tags")
    tag = relationship("Tag", backref="course_tags")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)


def add_record(table, **kwargs):
    session = Session()
    new_data = table(**kwargs)
    session.add(new_data)
    session.commit()
    session.close()
    return new_data


def get_record(table, **kwargs):
    session = Session()
    query = session.query(table)
    if kwargs:
        for attr, value in kwargs.items():
            query = query.filter(getattr(table, attr) == value)
        data = query.all()
        if len(data) == 1:
            data = data[0]
    else:
        data = query.all()
        if len(data) == 1:
            data = data[0]
    session.close()
    return data
