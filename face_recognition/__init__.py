# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.orm import column_property


app = Flask(__name__)

app.config['SECRET_KEY'] = '06e75a791a70762eceaf95828c208db2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proj_database.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)                            # making bcrypt object
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from face_recognition import routes

# __author__ = """Adam Geitgey"""
# __email__ = 'ageitgey@gmail.com'
# __version__ = '1.2.3'

from .api import load_image_file, face_locations, batch_face_locations, face_landmarks, face_encodings, compare_faces, face_distance
