from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Table, Column, func

from datetime import datetime

class Model(DeclarativeBase):

    # можно тут добавить тогда эти столбцы будут во всех таблицах
   # т.к. мы наследуемся от этого класса
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # будет вписывать дататайм при создании записи
    dateCreate: Mapped[datetime] = mapped_column(        
                                        server_default=func.now(),
                                        nullable=False)
    
    # будет вписывать дататайм при обновлении записи
    dateUpdate: Mapped[datetime] = mapped_column(        
                                        server_default=func.now(),
                                        server_onupdate=func.now(),
                                        nullable=False)


class UserOrm(Model):
    __tablename__ = 'user'
    
    # уже не нужен так как наследуется
    # id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]
    # quiz = relationship('QuizOrm', backref='user')
