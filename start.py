from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

#Class with user data
class UserInfo():
    data = pd.read_csv('./games.csv')


user = UserInfo()

#Init flask app and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

#Users table in database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


@app.route('/')
def index():
    return render_template('index.html')

#Table page
@app.route('/table')
def table():
    return render_template(
        'table.html',
        data=user.data.head(10),
        len=len(user.data.columns)
    )

#Change table values
@app.route('/table/change_table', methods=['POST'])
def change_table():
    index = request.form['index']
    column = request.form['column']
    value = request.form['value']
    if index.isdigit():
        index = int(index)
    user.data.loc[index, column] = value
    return '0'

#Check login
@app.route('/check_login', methods=['POST'])
def check_login():
    login = request.form['login']
    if User.query.filter_by(username=login).first() is None:
        return 'None'
    else:
        return 'Find'

#Add account
@app.route('/add_account', methods=['POST'])
def add_account():
    login = request.form['login']
    password = request.form['password']
    db.session.add(User(username=login, password=password))
    db.session.commit()
    response = make_response('Success')
    response.set_cookie('login', login)
    return response

#Authorization
@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    if User.query.filter_by(username=login, password=password).first() is None:
        return 'None'
    else:
        response = make_response('Success')
        response.set_cookie('login', login)
        return response


@app.route('/add_database_table')
def add_table():
    db.create_all()


@app.route('/get_cookie')
def get_cookie():
    login = request.cookies.get('login')
    return "cookie: " + login
