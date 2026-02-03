from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from example.sqlalchemy_help.models_one_to_many import add_data, User, PhoneNumber


# engine = create_engine('sqlite:///test2.db', echo=True) # sql запросы в консоль
engine = create_engine('sqlite:///test2.db')


# до v.2.0
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(autoflush=False, bind=engine)

# Base.metadata.create_all(engine)

with Session(autoflush=False, bind=engine) as db:
    # Метод flush() синхронизирует все сделанные изменения в объектах с 
    #       базой данных, то есть отправляет SQL-инструкции 
    #       (INSERT/UPDATE/DELETE) в БД, не завершая транзакцию (без commit).
    #       Такая промывка нужна, чтобы запросы видели актуальное состояние данных, 
    #       включая только что изменённые или добавленные объекты.
    
    add_data(engine, db)
    
    users = db.query(User).all()
    for user in users:
        print(user.fname, user.age)
    
    user = db.get(User, 1) 
    print(user)   
    print(user.phones[0].number) 
    for ph in user.phones:
        print(ph.number)  
    
    
    # user = db.query(User).filter_by(id=2).one()    
    # users = db.query(User).filter(User.id>3).all()
    
    # from sqlalchemy import or_
    # users = db.query(User).filter(or_(User.fname=='Max1', User.fname=='Max2')).all()
    # print(users)
    
    # users = db.query(User).filter(User.fname.like(r'%ax6%')).all()
    # print(users)
    
    
    # # ------  UPDATE  ----
    # user = db.get(User, 1)    
    # user.fname = "Gerald"
    # user.phones.append(PhoneNumber('12345678', 'mts'))       
    # user.phones[0].number = '99999999'
    # db.commit()
    
    # user = db.get(User, 1)    
    # print(user)
    # print(*user.phones, sep='\n')
    
    
    
    # # ------  DELETE  ----    
    # user = db.get(User, 1)    
    # db.delete(user)    
    # db.commit()
    
    # user = db.get(User, 6)    
    # print(user.phones)
    # user.phones.pop()
    # print(user.phones)
    
    
    # user = db.get(User, 7)    
    # print(user.phones)
    # phone = user.phones[0]
    # user.phones.remove(phone)
    # print(user.phones)
    
    
    

    # ----------------------- pydantic
    
    # input_user_json = """
    # {        
    #     "fname": "John",
    #     "lname": "Doe",
    #     "gender": "Male",
    #     "age": 30,    
    #     "phones": [
    #         {"phone_type": "Мобильный", "number": "1111111111"},
    #         {"phone_type": "Рабочий", "number": "222222222"}
    #     ]
    # }"""
    
    # from schemas import UserSchema
    
    # user_s = UserSchema.model_validate_json(input_user_json) # проверка (валидация)
    # print('----------')
    # print(user_s)
    # phones = [PhoneNumber(**phone.model_dump()) for phone in user_s.phones]
    # user_s.phones = []    
    # user = User(**user_s.model_dump())    
    # print(user)
    # user.phones += phones
    # db.add(user)
    # db.commit()
    # print(user)
        