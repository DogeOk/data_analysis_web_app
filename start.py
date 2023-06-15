from flask import Flask, render_template,\
    request, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
import plotly
from werkzeug.utils import secure_filename
import pandas as pd
from ydata_profiling import ProfileReport
import os
import re
import io
import json
import multiprocessing


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


def get_profile_report(profile):
    pd.options.plotting.backend = "matplotlib"
    return profile.to_html()


@app.route('/table/profile_report')
def table_profile_report():
    login = request.cookies.get('login')
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        report = p.map(
            get_profile_report,
            [ProfileReport(users[login].data, title='Подробный отчёт')]
        )
    return report[0]


# Change table values
@app.route('/table/change_table', methods=['POST'])
def change_table():
    login = request.cookies.get('login')
    index = request.form['index']
    column = request.form['column']
    value = request.form['value']
    if index.isdigit():
        index = int(index)
    if value.isdigit():
        users[login].data.loc[index, column] = int(value)
        return 'Success'
    try:
        users[login].data.loc[index, column] = float(value)
    except ValueError:
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


@app.route('/table/replace_values', methods=['POST'])
def replace_values():
    login = request.cookies.get('login')
    find = request.form['findValue']
    if find.isdigit():
        find = float(find)
    replace = request.form['replaceValue']
    if replace.isdigit():
        replace = float(replace)
    column = request.form['columnReplace']
    users[login].data[column] = users[login].data[column].apply(
        lambda value: replace if value == find else value
    )
    return '<script>window.location.replace("/");</script>'


@app.route('/table/create_pivot_table', methods=['POST'])
def create_pivot_table():
    login = request.cookies.get('login')
    index = request.form['pivotTableIndex']
    values = request.form['pivotTableValues']
    func = request.form['pivotTableFunction']
    open_new_table = request.form.get('pivotTableOpen')
    file_name = request.form['pivotTableSaveName']
    new_pivot_table = users[login].data.pivot_table(
        index=index,
        values=values,
        aggfunc=func
    ).reset_index()
    if file_name[-4:] != '.csv':
        file_name = file_name + '.csv'
    new_pivot_table.to_csv(
        f'./users_files/{login}/{file_name}',
        index=False
    )
    if open_new_table == 'on':
        users[login].data = new_pivot_table
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


# Logout from account
@app.route('/logout')
def logout():
    response = make_response('<script>window.location.replace("/");</script>')
    response.delete_cookie('login')
    del users[request.cookies.get('login')]
    return response


# Return list of user files
@app.route('/user_files')
def user_files():
    login = request.cookies.get('login')
    if login is None:
        return 'Error'
    files = [file for file in os.listdir(f"./users_files/{login}")]
    return files


# Upload user file
@app.route('/upload_file', methods=['POST'])
def upload_file():
    login = request.cookies.get('login')
    file = request.files['user_file']
    file.save(f'./users_files/{login}/{secure_filename(file.filename)}')
    return 'Success'


# Open user file
@app.route('/open_file', methods=['POST'])
def open_file():
    filename = request.form['file_name']
    login = request.cookies.get('login')
    users[login].file_path = f'./users_files/{login}/{filename}'
    users[login].data = pd.read_csv(users[login].file_path)
    return 'Success'


# Delete user file
@app.route('/delete_file', methods=['POST'])
def delete_file():
    filename = request.form['file_name']
    login = request.cookies.get('login')
    os.remove(f'./users_files/{login}/{filename}')
    return 'Success'


# Save user file in server
@app.route('/save_file', methods=['POST'])
def save_file():
    login = request.cookies.get('login')
    file_name = request.form['fileName']
    if file_name == ':':
        users[login].data.to_csv(users[login].file_path, index=False)
    else:
        if file_name[-4:] != '.csv':
            file_name = file_name + '.csv'
        users[login].data.to_csv(
            f'./users_files/{login}/{file_name}',
            index=False
        )
    return 'Success'


# Export user file
@app.route('/download_file')
def download_file():
    login = request.cookies.get('login')
    return send_file(users[login].file_path)


# Create graphs
@app.route('/graph', methods=['POST'])
def graph():
    login = request.cookies.get('login')
    x = request.form['xGraph']
    y = request.form['yGraph']
    graph_type = request.form['graphType']
    graph_title = request.form['graphName']
    fig = users[login].data.plot(kind=graph_type, x=x, y=y, title=graph_title)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html', graphJSON=graphJSON)
