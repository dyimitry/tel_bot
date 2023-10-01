import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session


Base = declarative_base()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
session = Session(engine)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(200))
    user_surname = Column(String(200))
    username = Column(String(200))

    def __str__(self):
        # При вызове функции print()
        # будут выводиться значения полей pep_number и name.
        return f'{self.user_id}'


Base.metadata.create_all(engine)


