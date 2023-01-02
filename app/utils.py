#%%
import sqlite3 as sql
import re

# connect to qa_database.sq (database will be created, if not exist)
def create_table_if_not_exist(db_name :str, db_table : str):
    con = sql.connect(db_name)
    con.execute(f"CREATE TABLE IF NOT EXISTS {db_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT, Email TEXT, Password TEXT, Username TEXT)")
    con.close()


# Register new user
def register_user(db_name : str, db_table : str, values : list[str, str, str]):
    """Registra un nuevo usuario en la base de datos
        db_name = nombre d ela base de datos
        db_table = nombre de la tabla
        username = nombre del usuario
        email = email de usuario
        password = contraseña del usuario

        Returns: 
        - False: si encontramos error
        - True: si no encontramos error
    """
    username, email, password = values
    
    query = f"SELECT * FROM {db_table} WHERE username ='{username}' OR email = '{email}'"# AND password = '{password}' "
    account = send_query_with_response(db_name, query)
    print(account, username, email, password)
    if account != sql.Error:
        if account:
            msg = 'El email o username ya existen. Vuelvo a intentarlo.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]', email):
            msg = 'Invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            query = f"INSERT INTO {db_table} (username, email, password) VALUES ('{username}','{email}', '{password}')"
            response = send_query_within_response(db_name, query)
            if response == sql.Error:
                msg = 'Error'
            else:
                return True, 'You have successfully registered' 

    return False, msg


# Log user
def login_user(db_name : str, db_table : str, values : list[str, str]):
    pass
# Log out user
def logout_user(db_name : str, db_table : str, values : list[str, str]):
    pass

def connect_database(db_name : str):
    connection = sql.connect(db_name)    
    cursor =  connection.cursor() # cursor
    # insert data
    return connection, cursor

def send_query_within_response(db_name : str ,query : str):
    try:
        con, c = connect_database(db_name)       
        c.execute(query) 
        con.commit() # apply changes
    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return err
    finally:
        con.close() # close the connection

def send_query_with_response(db_name : str, query : str, isAll : bool = False):
    """Si el isAll es falso, significa que solo queremos un valor. DE lo contrario
        devolveremos todos los valores que encontremos.
    """
    try:
        con, c = connect_database(db_name)
        c.execute(query)  
        if isAll:
            question = c.fetchall()
        else:
            question = c.fetchone()
        con.commit() # apply changes
        return question

    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return err
    finally:
        con.close() # close the connection

# Comprobamos que el nombre de las columnas 
def value_of_columns(db_name : str, db_table : str, name_cols : list[str]):
    if name_cols == []:
        return '*'
    try:
        query = f"SELECT * FROM {db_table}"
        con, cursor = connect_database(db_name)
        data = cursor.execute(query)  
        #data = cursor.description
        lst_col =  [col[0].lower() for col in data.description]
        for col in name_cols:
            if col.lower() not in lst_col:
                return con.Error(f"{col} is invalid")
        return ", ".join(name_cols)

    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return err
    finally:
        con.close() # close the connection

def select(db_name : str, db_table : str, name_cols : list[str], id = 0):
    val_cols = value_of_columns(db_name, db_table, name_cols)
    if val_cols != sql.Error:
        if id > 0: query = f"SELECT {val_cols} FROM {db_table} WHERE id = {id}"
        else: query = f"SELECT {val_cols} FROM {db_table}"
        response = send_query_with_response(db_name, query, id == 0)
        return response
    else: return val_cols

def update(db_name : str, db_table : str, values : list[str], id: int):
    question, answer = values
    response = select(db_name, db_table, [], id)
    if response:
        query = f"UPDATE {db_table} SET question='{question}', answer='{answer}' where id = {id}"
        flag = send_query_within_response(db_name, query)
        return flag
    else:
        return sql.Error(f"Id {id} doesn't exist in the table {db_table}")

def delete(db_name : str, db_table : str, id : int):
    query = f"DELETE FROM {db_table} WHERE id = {id}"    
    flag = send_query_within_response(db_name, query)
    return flag

def insert(db_name : str, db_table : str, values : list[str]):
    question, answer = values 
    query = f"INSERT INTO {db_table} (question, answer) VALUES ('{question}','{answer}')"
    flag = send_query_within_response(db_name, query)
    return flag
# %%
