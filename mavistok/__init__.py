from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='mavi'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/mavi_stok'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from mavistok.models import Users
from mavistok import routes