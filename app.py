from flask import Flask, request, render_template, redirect, session, url_for
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum, Text, select
import os
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField, validators, RadioField, FormField, \
    SubmitField, FieldList, TextAreaField, BooleanField
from wtforms.validators import DataRequired, InputRequired

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
    user_role = Column(Enum('admin', 'student', 'professor', name='user_roles'), nullable=False)
    f_name = Column(String(100), nullable=False)
    l_name = Column(String(100), nullable=False)

    professor = relationship('Professor', uselist=False, backref='user', cascade="all, delete")
    student = relationship('Student', uselist=False, backref='user', cascade="all, delete")


class Professor(Base):
    __tablename__ = 'professors'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    degree = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)

    subjects_taught = relationship('ClassSubject', backref='professor')
    quizzes_created = relationship('Quiz', backref='creator', uselist=False)


class Student(Base):
    __tablename__ = 'students'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.class_id'), nullable=False)

    class_ = relationship('Class', backref='student')
    quiz_results = relationship('QuizResult', backref='student')
    answers_given = relationship('StudentAnswer', backref='student')


class Class(Base):
    __tablename__ = 'classes'
    class_id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(255), unique=True, nullable=False)
    class_field = Column(String(255), nullable=False)
    class_level = Column(Integer, nullable=False)

    students_in = relationship('Student', backref='class')
    subjects = relationship('ClassSubject', backref='class')
    quizzes = relationship('ClassQuiz', backref='classes')


class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    sub_name = Column(String(255), unique=True, nullable=False)

    classes_profs = relationship('ClassSubject', backref='subject')
    quizzes = relationship('Quiz', backref='subject')


class ClassSubject(Base):
    __tablename__ = 'class_subjects'
    class_id = Column(Integer, ForeignKey('classes.class_id'), primary_key=True, nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), primary_key=True, nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.user_id'))


class Quiz(Base):
    __tablename__ = 'quizzes'
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_name = Column(String(255), nullable=False)
    description = Column(String(300))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    prof_id = Column(Integer, ForeignKey('professors.user_id'), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)
    attempts = Column(Integer)

    questions = relationship('Question', backref='quiz')
    results = relationship('QuizResult', backref='quiz')
    classes = relationship('ClassQuiz', backref='quizzes')


class Question(Base):
    __tablename__ = 'questions'
    q_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False)
    q_content = Column(Text, nullable=False)

    options = relationship('Option', backref='question')

    def is_answer_correct(self, selected_option_ids):
        # Get the correct option IDs for this question
        correct_option_ids = [option.option_id for option in self.options if option.is_correct]

        # Check if the selected option IDs match the correct option IDs
        return set(selected_option_ids) == set(correct_option_ids)


class Option(Base):
    __tablename__ = 'options'
    option_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.q_id'), nullable=False)
    o_content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)


class QuizResult(Base):
    __tablename__ = 'quiz_results'
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.user_id'), primary_key=True, nullable=False)
    score = Column(Float, nullable=False)
    attempt = Column(Integer, nullable=False)
    completed_at = Column(DateTime, nullable=False)


class StudentAnswer(Base):
    __tablename__ = 'student_answers'
    student_id = Column(Integer, ForeignKey('students.user_id'), primary_key=True, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.q_id'), primary_key=True, nullable=False)
    option_id = Column(Integer, ForeignKey('options.option_id'), nullable=False)


class ClassQuiz(Base):
    __tablename__ = 'class_quiz'
    class_id = Column(Integer, ForeignKey('classes.class_id'), nullable=False, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=False, primary_key=True)


# ------------------------------------Define the forms--------------------------------------


class ProfessorForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    professor_id = HiddenField('Professor ID')


class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    class_id = SelectField('Class', choices=[], coerce=int, validators=[DataRequired()])
    student_id = HiddenField('Student ID')


class OptionForm(FlaskForm):
    o_content = StringField('Option Content')
    is_correct = BooleanField('Is Correct?')


class QuestionForm(FlaskForm):
    q_content = StringField('Question Content', validators=[DataRequired()])
    options = FieldList(FormField(OptionForm), min_entries=4)


class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    subject_id = SelectField('Subject', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Next')


# -------------------------------------------Define functions-----------------------------------------------------


# Delete users (professor, student, admin)


def delete(user_id):
    # Find the user by id
    user = session0.query(User).get(user_id)
    # Delete the user from the database
    session0.delete(user)
    session0.commit()


# Load professors


def load_professors():
    professors = session0.query(Professor).all()
    return professors


# load students


def load_students():
    query = select(User.username, User.f_name, User.l_name, Class.class_name, User.user_id).select_from(User). \
        join(Student).join(Class)

    # Execute the query and fetch the results
    result = session0.execute(query)
    students = result.fetchall()
    session0.commit()
    return students


# load classes
def load_classes():
    classes = session0.query(Class).all()
    session0.commit()
    return classes


# Get professor by ID


def get_professor(professor_id):
    professor = session0.query(Professor).get(professor_id)
    session0.commit()
    return professor


# Get student by ID


def get_student(student_id):
    student = session0.query(Student).get(student_id)
    session0.commit()
    return student


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


# edit student


def edit_stu(student, form):
    username = form.username.data
    password = form.password.data
    f_name = form.f_name.data
    l_name = form.l_name.data
    class_id = form.class_id.data

    # Update the professor details
    student.class_id = class_id

    # Find the associated user and update their details
    user = student.user
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


# fill the edit student form with the current data


def fill_student_form(student, form):
    form.username.data = student.user.username
    form.password.data = student.user.user_password
    form.f_name.data = student.user.f_name
    form.l_name.data = student.user.l_name
    form.class_id.data = student.class_id
    form.student_id.data = student.user_id


def load_subject_by_prof(prof_id):
    class_subjects = session0.query(ClassSubject).filter(ClassSubject.professor_id == prof_id).all()

    # Retrieve the subject_ids from the ClassSubject objects
    subject_ids = [cs.subject_id for cs in class_subjects]

    # Query the Subject table to get the subject names for the retrieved subject_ids
    subjects = session0.query(Subject).filter(Subject.subject_id.in_(subject_ids)).all()
    session0.commit()
    return subjects


def add_question_to_database(quiz_id, question_content, options_data):
    # Create a new Question instance and add it to the database
    new_question = Question(quiz_id=quiz_id, q_content=question_content)
    session0.add(new_question)
    session0.commit()

    # Retrieve the question ID (assuming the primary key is auto-incremented)
    question_id = new_question.q_id

    # Create Option instances and add them to the database
    for option_content, is_correct in options_data:
        new_option = Option(question_id=question_id, o_content=option_content, is_correct=is_correct)
        session0.add(new_option)

    # Commit the changes to the database
    session0.commit()


def get_quiz_by_id(quiz_id):
    quiz = session0.query(Quiz).get(quiz_id)
    return quiz


def get_class_sub_prof(professor_id,subject_id):
    class_subjects = session0.query(ClassSubject).filter_by(professor_id=professor_id,subject_id=subject_id)
    classes_ids = [class_subject.class_id for class_subject in class_subjects]
    classes = session0.query(Class).filter(Class.class_id.in_(classes_ids)).all()
    session0.close()
    return classes


def get_quiz_subject(quiz_id):
    quiz = session0.query(Quiz).get(quiz_id)
    sub_id = quiz.subject_id
    session0.close()
    return sub_id
# ----------------------Routes and view functions---------------------------------


# Professor's account-----------------------


@app.route('/create_quiz/', methods=['GET', 'POST'])
def create_quiz_info():
    form = QuizForm()
    prof_id = session['user_id']
    subjects = load_subject_by_prof(prof_id)
    form.subject_id.choices = [(s.subject_id, s.sub_name) for s in subjects]
    if form.validate_on_submit():
        # Retrieve data from the form
        title = form.title.data
        desc = form.description.data
        subject_id = form.subject_id.data

        # Create a new user entry in the 'users' table
        # and a new professor entry in the 'student' table
        # Save the changes to the database
        quiz = Quiz(quiz_name=title,
                    description=desc,
                    subject_id=subject_id,
                    prof_id=prof_id)
        session0.add(quiz)
        session0.commit()
        quiz_id = quiz.quiz_id

        return redirect('/create_question/' + str(quiz_id))
    return render_template('create_quiz.html', form=form)


@app.route('/create_question/<int:quiz_id>', methods=['GET', 'POST'])
def create_question(quiz_id):
    quiz = get_quiz_by_id(quiz_id)
    return render_template('create_question.html', quiz=quiz)


@app.route('/save_question/<int:quiz_id>', methods=['GET', 'POST'])
def save_question(quiz_id):
    # Get the form data
    q_content = request.form.get('q_content')
    o_content_1 = request.form.get('o_content_1')
    o_content_2 = request.form.get('o_content_2')
    o_content_3 = request.form.get('o_content_3')
    o_content_4 = request.form.get('o_content_4')
    is_correct_1 = request.form.get('is_correct_1') == 'on'
    is_correct_2 = request.form.get('is_correct_2') == 'on'
    is_correct_3 = request.form.get('is_correct_3') == 'on'
    is_correct_4 = request.form.get('is_correct_4') == 'on'

    # Create a question instance with the question content
    question = Question(quiz_id=quiz_id,q_content=q_content)

    # Create option instances with the option content and status
    option_1 = Option(o_content=o_content_1, is_correct=is_correct_1)
    option_2 = Option(o_content=o_content_2, is_correct=is_correct_2)

    # Associate the options with the question
    question.options = [option_1, option_2]

    # Check if option 3 is filled
    if o_content_3:
        # Create an option instance with the option content and status
        option_3 = Option(o_content=o_content_3, is_correct=is_correct_3)
        # Add the option to the question options
        question.options.append(option_3)

    # Check if option 4 is filled
    if o_content_4:
        # Create an option instance with the option content and status
        option_4 = Option(o_content=o_content_4, is_correct=is_correct_4)
        # Add the option to the question options
        question.options.append(option_4)

    # Add the question and the options to the database session
    session0.add(question)
    session0.commit()
    action = request.form.get('action')

    if action == 'add_question':
        # Call the create_question function
        return redirect('/create_question/' + str(quiz_id))
    elif action == 'save_quiz':
        return redirect('/quiz_more_info/' + str(quiz_id))


@app.route('/quiz_more_info/<int:quiz_id>')
def quiz_more_info(quiz_id):
    quiz = get_quiz_by_id(quiz_id)
    sub_id = get_quiz_subject(quiz_id)
    prof_id = session['user_id']
    classes = get_class_sub_prof(prof_id, sub_id)
    return render_template('save_quiz.html', quiz=quiz, classes=classes)

@app.route('/save_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def save_quiz(quiz_id):

    return redirect('/')
# Dashboard------------------------------


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['user_role'] != 'admin':
        return redirect('/home/' + str(session['user_id']))
    classes = session0.query(Class).all()
    students = load_students()
    professors = load_professors()
    return render_template('dashboard.html',
                           professors=professors,
                           students=students,
                           classes=classes)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def sup_user(user_id):
    delete(user_id)
    return redirect('/dashboard')


@app.route('/add_professor', methods=['POST'])
def add_professor():
    form = ProfessorForm()
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
            '/dashboard')
    return render_template('add_professor.html', form=form)


@app.route('/add_student', methods=['POST'])
def add_student():
    form = StudentForm()
    classes = load_classes()
    form.class_id.choices = [(c.class_id, c.class_name) for c in classes]
    if form.validate_on_submit():
        # Retrieve data from the form
        username = form.username.data
        password = form.password.data
        f_name = form.f_name.data
        l_name = form.l_name.data
        class_id = form.class_id.data

        # Create a new user entry in the 'users' table
        # and a new professor entry in the 'student' table
        # Save the changes to the database
        user = User(username=username,
                    user_password=password,
                    user_role='student',
                    f_name=f_name,
                    l_name=l_name)
        student = Student(class_id=class_id)
        user.student = student
        session0.add(user)
        session0.commit()

        return redirect('/dashboard')
    return render_template('add_student.html', form=form)


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


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    # Get the professor from the database
    student = get_student(student_id)
    if not student:
        # If the student is not found, redirect to the dashboard page
        return redirect('/dashboard')

    form = StudentForm()
    classes = load_classes()
    form.class_id.choices = [(c.class_id, c.class_name) for c in classes]

    if form.validate_on_submit():
        edit_stu(student, form)
        return redirect('/dashboard')

    # Populate the form fields with the professor's current data
    fill_student_form(student, form)

    return render_template('edit_stu.html', form=form, student=student)


@app.route('/home/<int:user_id>')
def home(user_id):
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
