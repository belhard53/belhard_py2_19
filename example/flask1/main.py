from flask import Flask, jsonify, render_template
import os

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# def f1():
#     pass
# app.add_url_rule('/', f1)


users=['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666']

@app.route('/')
def index():
    # return "Hello FLASK"
    return render_template('index.html', 
                           name="Vasya1", 
                           title="Some title", 
                           image = 'bear')

@app.route('/users/')
def users_():    
    return render_template(
        'users.html', 
        users=users, len=len # отдельно передаем функцию len
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

@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red"> такой страницы не существует </h1>'

app.run(debug=True)