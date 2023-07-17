# from database.db import db


# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(255), unique=True, nullable=False)
#   user_password = db.Column(db.String(255), nullable=False)
#   user_role = db.Column(db.Enum('admin', 'student', 'professor'),
#                         nullable=False)
#   f_name = db.Column(db.String(100), nullable=False)
#   l_name = db.Column(db.String(100), nullable=False)


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Enum('admin', 'student', 'professor'), nullable=False)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
