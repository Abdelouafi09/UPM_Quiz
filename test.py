from flask import Flask, request, render_template, redirect, session
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum, text
import os
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

#connecting to the database
db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})
Session = sessionmaker(bind=engine)
session0 = Session()
Base = declarative_base()

#Models


# Models
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    user_role = Column(Enum('admin', 'student', 'professor'), nullable=False)
    f_name = Column(String(100), nullable=False)
    l_name = Column(String(100), nullable=False)

    professor = relationship('Professor', uselist=False, backref='user', cascade="all, delete")
    students = relationship('Student', backref='user', cascade="all, delete")


class Professor(Base):
    __tablename__ = 'professors'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    degree = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)


class Student(Base):
    __tablename__ = 'students'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    class_ = relationship('Class', backref='students')


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(255), unique=True, nullable=False)
    class_field = Column(String(255), nullable=False)
    class_level = Column(Integer, nullable=False)



query = '''
    SELECT users.username, users.f_name, users.l_name, classes.class_name
    FROM users
    JOIN students ON users.user_id = students.user_id
    JOIN classes ON students.class_id = classes.id
'''

result = session0.execute(text(query))

students = []
for row in result:
    username, f_name, l_name, class_name = row
    students.append((username, f_name, l_name, class_name))
  
print(students)