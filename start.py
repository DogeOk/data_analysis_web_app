from flask import Flask, render_template,\
    request, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
import plotly
from werkzeug.utils import secure_filename
import pandas as pd
import os
import re
import io
import json


# Class with user data
class UserInfo():
    data = None
    file_name = None


users = {}

# Init flask app and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

# Pandas options
pd.options.plotting.backend = "plotly"


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


@app.route('/table/table_info')
def table_info():
    buffer = io.StringIO()
    login = request.cookies.get('login')
    users[login].data.info(buf=buffer)
    return buffer.getvalue()


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
    return 'Success'


# Delete columns from table
@app.route('/table/delete_column', methods=['POST'])
def delete_column():
    login = request.cookies.get('login')
    column = request.form['column']
    users[login].data = users[login].data.drop([column], axis=1)
    return 'Success'


# Delete rows from table
@app.route('/table/delete_row', methods=['POST'])
def delete_row():
    login = request.cookies.get('login')
    index = request.form['index']
    if index.isdigit():
        index = int(index)
    users[login].data = users[login].data.drop([index])
    return 'Success'


@app.route('/table/delete_skips', methods=['POST'])
def delete_skips():
    login = request.cookies.get('login')
    column = request.form['column']
    users[login].data = users[login].data[~users[login].data[column].isna()]
    return 'Success'


@app.route('/table/check_skips', methods=['POST'])
def check_skips():
    login = request.cookies.get('login')
    column = request.form['column']
    if column == ':':
        return str(users[login].data.isna().sum())
    return str(users[login].data[column].isna().sum())


@app.route('/table/delete_duplicates', methods=['POST'])
def delete_duplicates():
    login = request.cookies.get('login')
    column = request.form['column']
    if column == ':':
        users[login].data = users[login].data.drop_duplicates(keep='first')
    else:
        conditions = users[login].data[column].duplicated(keep='first')
        users[login].data = users[login].data[conditions]
    return 'Success'


@app.route('/table/check_duplicates', methods=['POST'])
def check_duplicates():
    login = request.cookies.get('login')
    column = request.form['column']
    if column == ':':
        return str(users[login].data.duplicated(keep='first').sum())
    else:
        return str(users[login].data[column].duplicated(keep='first').sum())


@app.route('/table/unique_values', methods=['POST'])
def unique_values():
    login = request.cookies.get('login')
    column = request.form['column']
    return ", ".join(map(str, users[login].data[column].unique()))


@app.route('/table/auto_rename_columns')
def auto_rename_columns():
    login = request.cookies.get('login')
    columns = map(lambda x: x.lower(), users[login].data.columns)
    columns = map(lambda x: re.sub(r' +', '_', x), columns)
    users[login].data.columns = list(columns)
    return '<script>window.location.replace("/");</script>'


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
    users[login].file_path = f'./users_files/{login}/{filename}'
    users[login].data = pd.read_csv(users[login].file_path)
    return 'Success'


@app.route('/delete_file', methods=['POST'])
def delete_file():
    filename = request.form['file_name']
    login = request.cookies.get('login')
    os.remove(f'./users_files/{login}/{filename}')
    return 'Success'


@app.route('/save_file')
def save_file():
    login = request.cookies.get('login')
    users[login].data.to_csv(users[login].file_path, index=False)
    return 'Success'


@app.route('/download_file')
def download_file():
    login = request.cookies.get('login')
    return send_file(users[login].file_path)


@app.route('/graph', methods=['POST'])
def graph():
    login = request.cookies.get('login')
    x = request.form['xGraph']
    y = request.form['yGraph']
    fig = users[login].data.plot.scatter(x=x, y=y)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html', graphJSON=graphJSON)
