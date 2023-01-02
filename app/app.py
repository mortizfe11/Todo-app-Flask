from flask import Flask
#from flaskext.mysql import MySQL

#mysql = MySQL()
app = Flask(__name__)

from routes import * 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug = True)