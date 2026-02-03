from flask import Flask, render_template, redirect, request, url_for, session
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key 12334 dslkfj dlskjf lsdkjf sdlkjflsdkjf'

r_num = 0

users=['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666', 'user77']
user = {'fname':'Vasya', 'lname':'Vasilyev'}

admin=True

# session['num'] = 0 #  так нельзя - можно только внутри ендпоинта (вью-функции)

@app.route("/")
def index():
    
    return render_template('index.html', admin=admin, user=user)


@app.route("/count/")
def count():
    # global r_num
    if not 'num' in session:
        session['num'] = 0
        
    
    session['num'] += 1
    return render_template('count.html', num=session['num'], admin=admin)

   
@app.route("/test/<int:num>/")
def test(num):    
    # return 'test ' * num
    return render_template('test.html', num=num, user=user, admin=admin)

@app.route("/users/", methods=['GET', 'POST'])
def users_():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            users.append(user_name)
            users.sort()
            return redirect(url_for('users_', _anchor=''))
            
    return render_template('users.html', user=user, len=len, users=users, admin=admin)


@app.route("/form1/", methods=['GET', 'POST'])
def form1():
    err = ''
    login = ''
    if request.method == 'POST':
        # query = request.args.get('q', '')  # args из get
        login = request.form.get('login')
        if login == 'qqq':
            return redirect(url_for('index')) # перенаправление по имени ендпоинта/вью-функции
        else:
            err='Пароль err'
    #     return render_template('form1.html', err='Пароль err')
    # else:
    return render_template('form1.html', err=err, login=login, user=user, admin=admin)

@app.route("/message/<login>/<mes>/")
def message(login, mes):
    return render_template("mes.html", user=login, mes=mes)


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'





app.run(debug=True)