from flask import render_template, request, session, redirect, url_for
from app import app
import sqlite3 as sql

from utils import *

app.secret_key = 'your secret key' 

db_name = "todo.db"
db_table = "users"
todos_table = "todos"
create_table_if_not_exist(db_name, [db_table, todos_table])

#%%%
type(sql.Error)
#%%

def detectErr(info):
    if type(info) == type(sql.Error):
        pass

# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("main.html", logged_in = session['logged_in'])

# Inicio de sesión o login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", logged_in = session['logged_in'])

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = login_user(db_name, db_table, [username, password])
        if account and account != sql.Error:
            session['logged_in'] = True
            session['id'] = account[0]
            session['username'] = account[-1]
            return render_template('profile.html', username = session['username'], logged_in = session['logged_in'])

        else:
            error = 'Wrong data.'
            return render_template('login.html', error=error, logged_in = session['logged_in'])

# Registro de usuario
@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", logged_in = session['logged_in'])

    elif request.method == 'POST':
        msg = ""
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']        
        can_register_user , msg= register_user(db_name, db_table, [username, email, password])
        if can_register_user:
            return render_template('register_thanks.html', username=username, msg=msg)
        else:
            return render_template('register.html', error=msg)
        
        #pass
# Perfil de usuario
@app.route("/profile/")
def profile():
    return render_template('profile.html', logged_in = session['logged_in'])


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('id', None)
    session.pop('username', None)
    session['logout_msg'] = "Has salido de sesión."
    return render_template('login.html', logout_msg=session['logout_msg'], logged_in = session['logged_in']) # redirect to login page

# Gestión de notas -> CRUD
    # Create -> Crear nota
    # Read -> Leer nota -> una o todas
    # Update -> Actualizar nota
    # Delete -> Eliminar nota

# Debe estar logeado -> ruta para ver TODAS las notas del usuario
@app.route("/todos/")
def get_all_todos():
    todos = read_all_todos(db_name, todos_table, session['id'])
    if todos != sql.Error:
        return render_template('todos.html', todos=todos, logged_in = session['logged_in'])
    return 'Todos' #mensaje de error

# Debe estar logeado -> ruta para ver UNA nota del usuario
@app.route("/todos/<int:id>")
def get_todo(id):
    todo = read_todo_by_id(db_name, todos_table, id) 
    if todo != sql.Error:
        return render_template('todo.html', todo = todo, logged_in = session['id'])
    return f"Todo {id}"

# Debe estar logeado -> ruta para crear una nota
@app.route("/create", methods=["GET", "POST"])
def create_todo():
    if request.method == 'GET':
        return render_template('create_todo.html', logged_in = session['logged_in'])

    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        done = 0 # 0 = Pendiente, 1 = Hecho/Completado
        can_create_todo = create_new_todo(db_name, todos_table, session['id'], [title, description, done]) 
        # Validar si se ha creado la nota con can_create_todo
        if can_create_todo != sql.Error:
            msg = 'Todo create correctly'        
            return render_template('create_thanks.html', msg=msg, logged_in = session['logged_in'])

# Debe estar logeado -> ruta para actualizar una nota
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_todo(id):
    if request.method == 'GET':
        todo = read_todo_by_id(db_name, todos_table, id)
        #si no error:
        return render_template("update_todo.html", todo=todo, logged_in = session['logged_in'])
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        done = int(request.form['done'])
        update_tod = update_todo_by_id(db_name, todos_table, session['id'], id, [title, description, done]) 
        msg = 'Update Thanks'
        return render_template('update_thanks.html', msg=msg, logged_in = session['logged_in'])

    return f"Update {id}"

# Debe estar logeado -> ruta para eliminar una nota
@app.route("/delete/<int:id>", methods=["GET", "DELETE"])
def delete_todo(id):
    if request.method == 'GET':
        msg = 'Delete Thanks'
        delete_tod = delete_todo_by_id(db_name, todos_table, session['id'], id)
        #si no error
        msg = 'Delete Thanks'
        return render_template('delete_thanks.html', msg=msg, logged_in = session['id'])

    return f"Delete {id}"

# Página de error
@app.errorhandler(404)
def page_not_found(e):
    return "Esta ruta no existe", 404