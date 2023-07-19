from flask import Flask, request, render_template, redirect, session
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum, text, select
import os
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

# connecting to the database
db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})
Session = sessionmaker(bind=engine)
session0 = Session()
Base = declarative_base()


# --------------------------------------Models-------------------------------------------------------------------


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


# -------------------------------------------Define functions-----------------------------------------------------

# Delete users (professor, student, admin)
def delete(user_id):
    # Find the user by id
    user = session0.query(User).get(user_id)
    # Delete the user from the database
    session0.delete(user)
    session0.commit()

# Add professor


def add_professor(form):
    if form.validate_on_submit():
        # Retrieve data from the form
        username = form.username.data
        password = form.password.data
        f_name = form.f_name.data
        l_name = form.l_name.data
        degree = form.degree.data
        specialization = form.specialization.data

        # Create a new user entry in the 'users' table
        # and a new professor entry in the 'professors' table
        # Save the changes to the database
        user = User(username=username,
                    user_password=password,
                    user_role='professor',
                    f_name=f_name,
                    l_name=l_name)
        professor = Professor(degree=degree, specialization=specialization)
        user.professor = professor
        session0.add(user)
        session0.commit()

        return redirect(
            '/dashboard')  # Redirect to a success page or desired route


# Load professors
def load_professors():
    professors = session0.query(Professor).all()
    return professors

# Get professor by ID

def get_professor(professor_id):
    professor = session0.query(Professor).get(professor_id)
    return professor


# Edit professor

def edit_prof(professor, form):
    username = form.username.data
    password = form.password.data
    f_name = form.f_name.data
    l_name = form.l_name.data
    degree = form.degree.data
    specialization = form.specialization.data

    # Update the professor details
    professor.degree = degree
    professor.specialization = specialization

    # Find the associated user and update their details
    user = professor.user
    user.username = username
    if password:
        user.user_password = password
    user.f_name = f_name
    user.l_name = l_name

    # Save the changes to the database
    session0.commit()

# fill the edit professor form with current data


def fill_prof_form(professor, form):
    form.username.data = professor.user.username
    form.password.data = professor.user.user_password
    form.f_name.data = professor.user.f_name
    form.l_name.data = professor.user.l_name
    form.degree.data = professor.degree
    form.specialization.data = professor.specialization
    form.professor_id.data = professor.user_id

# --------------------Define the forms------------------------


class ProfessorForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    professor_id = HiddenField('Professor ID')


# Routes and view functions



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form_prof = ProfessorForm()
    add_professor(form_prof)

    query = select(User.username, User.f_name, User.l_name, Class.class_name, User.user_id).select_from(User). \
        join(Student).join(Class)

    # Execute the query and fetch the results
    result = session0.execute(query)
    students = result.fetchall()
    professors = load_professors()
    return render_template('dashboard.html', form_prof=form_prof, professors=professors, students=students)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def sup_user(user_id):
    delete(user_id)
    return redirect('/dashboard')


@app.route('/edit_professor/<int:professor_id>', methods=['GET', 'POST'])
def edit_professor(professor_id):
    # Get the professor from the database
    professor = get_professor(professor_id)
    if not professor:
        # If the professor is not found, redirect to the dashboard page
        return redirect('/dashboard')

    form = ProfessorForm()

    if form.validate_on_submit():
        # Retrieve data from the form
        edit_prof(professor, form)
        return redirect('/dashboard')

    # Populate the form fields with the professor's current data
    fill_prof_form(professor, form)

    return render_template('edit_prof.html', form=form, professor=professor)





@app.route('/home/<int:id_user>')
def home(id_user):
    f_name = session.get('first_name')
    l_name = session.get('last_name')
    user_role = session.get('user_role')

    if user_role == 'student':
        return render_template('st_home.html', session=session)
    elif user_role == 'professor':
        return render_template('pr_home.html', session=session)
    elif user_role == 'admin':
        return redirect('/dashboard')
    else:
        return redirect('/login')


@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home/' + str(session['user_id']))
    else:
        return redirect('login')


@app.route('/home')
def nhome():
    if 'username' in session:
        return redirect('/home/' + str(session['user_id']))
    else:
        return redirect('login')


@app.route('/home/')
def nonhome():
    if 'username' in session:
        return redirect('/home/' + str(session['user_id']))
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/home/' + str(session['user_id']))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user based on the provided username
        user = session0.query(User).filter_by(username=username).first()

        # Check if a user was found and if the provided password matches
        if user and password == user.user_password:
            # Store the user's ID in the session to maintain the login state
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['first_name'] = user.f_name
            session['last_name'] = user.l_name
            session['user_role'] = user.user_role
            return redirect('/home/' + str(session['user_id']))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
