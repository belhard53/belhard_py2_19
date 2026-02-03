from sqlalchemy import Table, Column, Integer, ForeignKey, String, Enum, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase, Session

class Base (DeclarativeBase):
    pass

# Вспомогательная таблица для Many-to-Many между User и Group
user_group = Table(
    'user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


    # если вместо back_populates использовать  backref - можно не писать
    # users = relationship(
    #     'User',
    #     secondary=user_group,
    #     # back_populates='groups'
    # )
    
    def __repr__(self):
        return self.name

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    gender = Column(Enum('Male', 'Female', name='gender'), nullable=False)
    age = Column(Integer, nullable=False)

    groups = relationship(
        'Group',
        secondary=user_group,
        backref='users'
        # back_populates='users'
    )

    def __repr__(self):
        return self.fname 


engine = create_engine('sqlite:///test3.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(autoflush=False, bind=engine) as db:
    
    users = [
        User(fname = "Max4", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max5", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max6", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max7", lname="Maxovich", age=33, gender="Male"),
        User(fname = "Max8", lname="Maxovich", age=33, gender="Male")
     ]
    
    groups = [
        Group(name="group1"),
        Group(name="group2"),
    ]
    
    groups[0].users.append(users[0])
    groups[0].users.append(users[1])
    groups[0].users.append(users[2])
    groups[1].users.append(users[2])
    groups[1].users.append(users[3])
    groups[1].users.append(users[4])
    
    db.add_all(users)
    db.commit()
    
    users = db.query(User).all()
    for user in users:
        print(user.fname, user.groups)
        
    print('----------')
    gr = db.get(Group, 1)
    print(gr)
    print(gr.users)
    
    
    
    