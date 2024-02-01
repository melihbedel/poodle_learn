from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
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

    courses = relationship('Course', back_populates='teacher')


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    title = Column(String(45), nullable=False, unique=True)
    description = Column(String(45), nullable=False)
    objectives = Column(String(45), nullable=False)
    private = Column(Boolean, nullable=False)

    teacher = relationship('Teacher', back_populates='courses')
    sections = relationship('Section', back_populates='course')
    students = relationship('StudentSubscription', back_populates='course')
    tags = relationship('CourseTag', back_populates='course')


class Section(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(45), nullable=False)
    content = Column(String(45), nullable=False)
    description = Column(String(45))
    information = Column(String(45))

    course = relationship('Course', back_populates='sections')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)

    subscriptions = relationship('StudentSubscription', back_populates='student')


class StudentSubscription(Base):
    __tablename__ = 'student_subscriptions'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    student = relationship('Student', back_populates='subscriptions')
    course = relationship('Course', back_populates='students')


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String(45), nullable=False)

    courses = relationship('CourseTag', back_populates='tag')


class CourseTag(Base):
    __tablename__ = 'course_has_tags'
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    course = relationship('Course', back_populates='tags')
    tag = relationship('Tag', back_populates='courses')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




def add_record(session: Session, table: DeclarativeMeta, **kwargs):

    new_record = table(**kwargs)
    session.add(new_record)
    session.commit()
    return new_record
    
    

def get_record(session: Session, table: DeclarativeMeta, **kwargs) -> list:

    query = session.query(table)

    for key, value in kwargs.items():
        query = query.filter(getattr(table, key) == value)

    records = query.all()
    return records


# def add_teacher():
#     pass


# add_record(session, Student, email='another@mail.com', password='anotherpassword', first_name='Another', last_name='Student')

# students: list[Student] = get_records(session, Student, first_name='Melih')

# for student in students:
#     print(student.email, student.first_name)