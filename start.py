from flask import Flask, render_template, request
import pandas as pd


class UserInfo():
    data = pd.read_csv('./games.csv')


user = UserInfo()

app = Flask(__name__)


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
    user.data.loc[index, column] = value
    return '0'
