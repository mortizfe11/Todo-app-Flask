from flask import render_template, request
from app import app
import sqlite3 as sql

from utils import *

db_name = "todo.db"
db_table = "users"
create_table_if_not_exist(db_name, db_table)

# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("main.html")

# Inicio de sesión o login
@app.route("/login/")
def login():
    return render_template("login.html")

# Registro de usuario
@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']        
        can_register_user , msg= register_user(db_name, db_table, [username, email, password])
        print(can_register_user, msg)
        if can_register_user:
            return render_template('register_thanks.html', username=username, msg=msg)
        else:
            return render_template('register.html', error=msg)
        
        #pass
# Perfil de usuario
@app.route("/profile/")
def profile():
    return "Profile"

# Gestión de notas -> CRUD
    # Create -> Crear nota
    # Read -> Leer nota -> una o todas
    # Update -> Actualizar nota
    # Delete -> Eliminar nota

# Debe estar logeado -> ruta para ver TODAS las notas del usuario
@app.route("/todos/")
def get_all_todos():
    return "All Todos"

# Debe estar logeado -> ruta para ver UNA nota del usuario
@app.route("/todos/<int:id>")
def get_todo(id):
    return f"Todo {id}"

# Debe estar logeado -> ruta para crear una nota
@app.route("/create", methods=["GET", "POST"])
def create_todo():
    return "Create"

# Debe estar logeado -> ruta para actualizar una nota
@app.route("/update/<int:id>", methods=["GET", "PUT"])
def update_todo(id):
    return f"Update {id}"

# Debe estar logeado -> ruta para eliminar una nota
@app.route("/delete/<int:id>", methods=["GET", "DELETE"])
def delete_todo(id):
    return f"Delete {id}"

# Página de error
@app.errorhandler(404)
def page_not_found(e):
    return "Esta ruta no existe", 404