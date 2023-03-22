from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas as pd
import os


# Class with user data
class UserInfo():
    data = None


users = {}

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
    login = request.cookies.get('login')
    if login is not None:
        if login not in users.keys():
            users[login] = UserInfo()
    else:
        return render_template(
            'table.html',
            login_none=True
        )
    if users[login].data is None:
        data = None
        length = None
    else:
        data = users[login].data.head(10)
        length = len(users[login].data.columns)
    return render_template(
        'table.html',
        data=data,
        len=length,
        login=login,
        data_none=data is None,
        login_none=login is None
    )


# Change table values
@app.route('/table/change_table', methods=['POST'])
def change_table():
    login = request.cookies.get('login')
    index = request.form['index']
    column = request.form['column']
    value = request.form['value']
    if index.isdigit():
        index = int(index)
    users[login].data.loc[index, column] = value
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
    users[login] = UserInfo()
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
        users[login] = UserInfo()
        return response


@app.route('/logout')
def logout():
    response = make_response('<script>window.location.replace("/");</script>')
    response.delete_cookie('login')
    del users[request.cookies.get('login')]
    return response


@app.route('/user_files')
def user_files():
    login = request.cookies.get('login')
    if login is None:
        return 'Error'
    files = [file for file in os.listdir(f"./users_files/{login}")]
    return files


@app.route('/upload_file', methods=['POST'])
def upload_file():
    login = request.cookies.get('login')
    file = request.files['user_file']
    file.save(f'./users_files/{login}/{secure_filename(file.filename)}')
    return 'Success'


@app.route('/open_file', methods=['POST'])
def open_file():
    filename = request.form['file_name']
    login = request.cookies.get('login')
    users[login].data = pd.read_csv(f'./users_files/{login}/{filename}')
    return 'Success'


@app.route('/get_cookie')
def get_cookie():
    login = request.cookies.get('login')
    return "cookie: " + str(login)
