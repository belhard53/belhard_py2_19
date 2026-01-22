from flask import (Flask, jsonify, render_template, 
                    session, request, redirect, url_for)
import os


# Flask по умолчанию хранит данные сессий на стороне клиента в виде файла cookie. 
# Однако, для обеспечения безопасности, Flask использует подписанные cookie, 
# что означает, что данные сессии шифруются и проверяются на целостность с 
# помощью секретного ключа, который хранится на сервере.

# Если нужно хранить данные сессий на сервере (например, для более сложных 
# приложений или когда вы не хотите доверять клиенту), вы можете использовать 
# сторонние расширения, такие как Flask-Session. Это расширение позволяет 
# хранить сессии в различных хранилищах, таких как файловая система, 
# Redis или база данных.


# модель MVC
    # model - модель данных из базы данных(будет позже)
    # view
    # controller
    

BASE_DIR = os.path.dirname(__file__) # так работает если проект открыт из любого места


app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# для сессий обязательно
app.config['SECRET_KEY'] = 'my secret key sadj;ask dj;askjd9032094u'

# def f1():
#     pass
# app.add_url_rule('/', f1)

# session['n'] = 0 #  так нельзя - можно только внутри ендпоинта (вью-функции)

users=['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666']

context = {"q":11, "w":22}

user = {'fname':'Vasya', 'lname':'Vasilyev'}

@app.route('/')
def index():
    # return "Hello FLASK"
    return render_template('index.html', 
                           name="Vasya1", 
                           title="Some title", 
                           image = 'bear',
                           user=user,
                           **context # q=11, w=22
                           )
                            

@app.route('/users/')
def users_():
    if False:
        return redirect(url_for('index'))       
    if not 'n' in session:
        session['n'] = 0
    session['n'] += 1
    
    # session['n'] - если 'n' нет - ошибка
    # session.get('n') - если 'n' нет - нет ошибки
    
    return render_template(
                'users.html', 
                users=users, 
                len=len, # отдельно передаем функцию len
                n=session['n']
    )    

@app.route('/test/<int:num>/')
def test(num):
    return f"test №{num}."




@app.route('/api/')
def f2():
    return jsonify({"name":"Vasya", "age":20})

@app.route("/message/<login>/<mes>/")
def message(login, mes):
    return render_template("message.html", user=login, mes=mes)

@app.route("/form1/", methods = ['GET', 'POST'])
def form1():
    login = ''
    err = ''
    if request.method == 'POST':
        err = ''
        print(request.form)    
        # print(11111111111111111, request.form.get('pass'))
        pas = request.form.get('pass', "")
        login = request.form.get('name', "")
        
        if len(login) < 3:
            err += 'login_err\n'
        if pas != '1234':
            err += 'password_err\n'
        
        if not err:
            return redirect(url_for('users_'))
        
        
    return render_template("form1.html", err=err, name=login)

@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red"> такой страницы не существует </h1>'

app.run(debug=True)