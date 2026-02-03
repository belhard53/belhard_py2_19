from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import os
from models import db, db_add_new_data, User

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')    


app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'


db.init_app(app)


# операции с БД перед запуском сервера
with app.app_context():
    db_add_new_data()
    # users = User.query.all()
    # users = User.query.filter(User.id>1).all()
    # print(users)
    # user = db.session.get(User, 1)
    # print(user)
    # print(user.quizes)
    
    
@app.route('/', methods = ['GET'])
def index():
    users = User.query.order_by(User.name).all()            
    return render_template('users.html', admin=True, len=len, users=users)
    


@app.route("/user_add/", methods=['GET', 'POST'])
def users_():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            user = User(user_name)
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('users_', _anchor=''))
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
    
    
app.run(debug=True)    