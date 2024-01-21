from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path

app = Flask(__name__)
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "6f3bd9a3-6474-4cbd-9ba6-3ff368e56637"

login_manager = LoginManager(app)
login_manager.login_view = "connexion"
