from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/poodle_learn')
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