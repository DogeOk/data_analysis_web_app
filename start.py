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


@app.route('/test')
def test():
    db.session.add(User(username='test12', password='test'))
    db.session.commit()
    print(User.query.all())
