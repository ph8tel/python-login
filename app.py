
from bottle import *
import db
import os

port = os.environ.get("PORT", 17995)

@route('<filename>')
def server_static(filename):
    return static_file(filename, root="/files")

@get('/')
def index():
    return template("index")

@post('/validator')
def validator():
    username = request.forms["username"]
    pwd = request.forms["password"]
    print("trying", username, pwd)
    login_status = db.validate(username, pwd)
    print(login_status)
    if login_status is not None:
        return template("dynamic")
    else:
        return template("rolled")

@get("/user_list")
def give_list():
    all_users = db.just_sql("SELECT * FROM users;")
    html_str = "<ol>"
    for user in all_users:
        html_str += f"<li id='{user[0]}'>{user[1]}</li>"
    return html_str + "</ol>"

@get("/remove_user/<username>")
def remove_user(username):
    db.remove_user(username)
    return give_list()

@post("/register")
def register():
    username = request.forms["username"]
    pwd = request.forms["password"]
    db.register(username,pwd)
    print("registering", username, pwd, db.validate(username,pwd))
    if db.validate(username,pwd) is not None:
        return template("rolled")
    else:
        return "reg fail"  + "<a href='/'>home</a>"

@get('/all')
def show_all_users():
    return str(db.just_sql("SELECT * FROM users;")) + "<a href='/'>all</a>"

run(host='0.0.0.0', port=port, debug = True)