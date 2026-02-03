from sqlalchemy import (Column, Integer, String, Enum, 
                                ForeignKey, DateTime, func)
from sqlalchemy.orm import relationship, DeclarativeBase


class Base (DeclarativeBase):
    id = Column(Integer, primary_key=True)
    
    # Время создания (устанавливается автоматически сервером)
    created_at = Column(DateTime(timezone=True), 
                        server_default=func.now(), 
                        nullable=False)
    
    # Время обновления (обновляется сервером при изменении записи)
    updated_at= Column(DateTime(timezone=True), 
                       server_default=func.now(), 
                       onupdate=func.now(), 
                       nullable=False)


class User(Base):
    __tablename__ = 'user'
    
    
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    gender = Column(Enum('Male', 'Female', name='gender'), nullable=False)
    age = Column(Integer, nullable=False)
    
    phones = relationship('PhoneNumber', backref='user')
    
    
    # def __init__(self, name, **kw):
    #     super().__init__(**kw)
    #     self.fname = name
    
    def __repr__(self):
        return f"User(id={self.id}, fname='{self.fname}'," \
               f"lname='{self.lname}', gender='{self.gender}', " \
               f"age={self.age}, phones={self.phones})"
    

class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'    
    
    
    phone_type = Column(String(20), nullable=False)
    number = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id')) # user.id - название таблицы    
    
    # если вместо back_populates использовать  backref - можно не писать
    # user = relationship('User', backref='phones')
    
    def __init__(self, number, phone_type, **kw):
        super().__init__(**kw)
        self.phone_type = phone_type
        self.number = number
        
    
    def __repr__(self):
        return f"PhoneNumber(id={self.id}, phone_type='{self.phone_type}', " \
                           f"number='{self.number}', user_id={self.user_id})"


def add_data(engine, db):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    user1 = User(fname='Max1', lname="Maxovich", age=22, gender='Male')
    user2 = User(fname='Max2', lname="Maxovich", age=22, gender='Male')
    user3 = User(fname='Max3', lname="Maxovich", age=22, gender='Male')
    # user2 = User('Max', "Maxovich", 22, 'Male') # с конструктором
    
    users = [
        User(fname = "Max4", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max5", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max6", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max7", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max8", lname="Maxovich", age=33, gender="Male")
     ]
    
    
    phone1 = PhoneNumber(phone_type = "type1", number='11111', user=user1)
    phone2 = PhoneNumber(phone_type = "type2", number='2222', user=user2)
    phone3 = PhoneNumber(phone_type = "type1", number='3333', user=users[0])
    phone4 = PhoneNumber(phone_type = "type2", number='4444', user=users[0])
    
    
    # db.add(user1)
    # db.add(user2)
    # db.add(user3)
    db.add_all(users + [user1, user2, user3])
    
    db.commit()
    
    