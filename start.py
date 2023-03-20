from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os


# Class with user data
class UserInfo():
    data = pd.read_csv('./games.csv')


user = UserInfo()

# Init flask app and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


# Users table in database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


# Table page
@app.route('/')
def table():
    if (not os.path.isfile('./instance/project.db')):
        db.create_all()
    return render_template(
        'table.html',
        data=user.data.head(10),
        len=len(user.data.columns),
        login=request.cookies.get('login')
    )


# Change table values
@app.route('/table/change_table', methods=['POST'])
def change_table():
    index = request.form['index']
    column = request.form['column']
    value = request.form['value']
    if index.isdigit():
        index = int(index)
    user.data.loc[index, column] = value
    return '0'


# Check login
@app.route('/check_login', methods=['POST'])
def check_login():
    login = request.form['login']
    if User.query.filter_by(username=login).first() is None:
        return 'None'
    else:
        return 'Find'


# Add account
@app.route('/add_account', methods=['POST'])
def add_account():
    login = request.form['login']
    password = request.form['password']
    db.session.add(User(username=login, password=password))
    db.session.commit()
    response = make_response('Success')
    response.set_cookie('login', login)
    os.makedirs(f'./users_files/{login}')
    return response


# Authorization
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


@app.route('/logout')
def logout():
    response = make_response('<script>window.location.replace("/");</script>')
    response.delete_cookie('login')
    return response


@app.route('/user_files')
def user_files():
    login = request.cookies.get('login')
    if login is None:
        return 'Error'
    files = [file for file in os.listdir(f"./users_files/{login}")]
    return files


@app.route('/get_cookie')
def get_cookie():
    login = request.cookies.get('login')
    return "cookie: " + str(login)
