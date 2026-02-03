# pip install flask-sqlalhemy

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    
    quizes = db.relationship('Quiz', backref='user', 
                             cascade = "all, delete, delete-orphan",
                             lazy='select')
    
     # lazy - 
            # select (по умолчанию)   Загружает всю коллекцию одним отдельным SELECT-запросом при первом обращении к атрибуту
            # joined  Загружает коллекцию сразу через JOIN с основной таблицей
            # subquery    Загружает коллекцию через подзапрос
            # dynamic Возвращает query-объект, коллекция не загружается сразу, можно строить запросы

    
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        
    def __repr__(self):
        return self.name

# отдельная таблица для связи many_to_many
quiz_question = db.Table('quiz_question',
            db.Column('quiz_ud', db.Integer, db.ForeignKey('quiz.id'), primary_key=True),
            db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
            )

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    # связь many_to_many прописываем только в одной из 2х таблиц
    # во второй появиться автоматом
    # если надо явно указать имя обратной связи во 2ой таблице тогда 
    # вместо backref - back_populates в обоих таблицах
    # question = db.relationship(
    #             'Question', 
    #             secondary=quiz_question, backref = 'quiz')

    def __init__(self, name: str, user:User) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return f'id - {self.id}, name - {self.name}'



class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)
    
    quiz = db.relationship(
                'Quiz', 
                secondary=quiz_question, backref = 'question')

    def __init__(self, quesion: str, answer, wrong1, wrong2, wrong3) -> None:
        super().__init__()
        self.question = quesion
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'{self.id}-{self.question}'    
    
def db_add_new_data():
    db.drop_all()
    db.create_all()    
    
    user1 = User('Петя')
    user2 = User('Вася')    
    
    # db.session.add(user1)
    db.session.add_all([user1, user2, User('_Коля')])
    
    
    db.session.commit()
        
    
    