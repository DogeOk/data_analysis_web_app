from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


class UserInfo():
    data = pd.read_csv('./games.csv')


user = UserInfo()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    return render_template(
        'table.html',
        data=user.data.head(10),
        len=len(user.data.columns)
    )


@app.route('/table/change_table', methods=['POST'])
def change_table():
    index = request.form['index']
    column = request.form['column']
    value = request.form['value']
    if index.isdigit():
        index = int(index)
    user.data.loc[index, column] = value
    return '0'


@app.route('/check_login', methods=['POST'])
def check_login():
    login = request.form['login']
    if User.query.filter_by(username=login).first() is None:
        return 'None'
    else:
        return 'Find'


@app.route('/add_account', methods=['POST'])
def add_account():
    login = request.form['login']
    password = request.form['password']
    db.session.add(User(username=login, password=password))
    db.session.commit()


@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    if User.query.filter_by(username=login, password=password).first() is None:
        return 'None'
    else:
        return 'Find'
