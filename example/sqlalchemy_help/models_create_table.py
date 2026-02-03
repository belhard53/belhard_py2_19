from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
class User2(Base):
    __tablename__ = 'users2'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)    

# Создание таблицы
from sqlalchemy import create_engine
engine = create_engine('sqlite:///example1.db')
Base.metadata.create_all(bind=engine)
    

        