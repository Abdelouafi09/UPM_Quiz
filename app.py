from flask import Flask, render_template, request, redirect, session
from database.db import load_users, load_subjects_for_professor
from sqlalchemy import  text


app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Set a secret key for session management

# Mock user data (replace with actual user retrieval from the database)


@app.route('/')
def index():
  if 'username' in session:
    return redirect('/home/' + str(session['id_user']))
  else:
    return redirect('login')


@app.route('/home')
def nhome():
  if 'username' in session:
    return redirect('/home/' + str(session['id_user']))
  else:
    return redirect('login')


@app.route('/home/')
def nonhome():
  if 'username' in session:
    return redirect('/home/' + str(session['id_user']))
  else:
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect('/home/' + str(session['id_user']))
  else:
    users = load_users()
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      user = next(
        (user for user in users
         if user['username'] == username and user['password'] == password),
        None)
      if user:
        session['id_user'] = user['id_user']
        session['first_name'] = user['f_name']
        session['last_name'] = user['l_name']
        session['username'] = user['username']
        session['user_role'] = user['role']
        return redirect('/home/' + str(session['id_user']))
      else:
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)
    return render_template('login.html')


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
    return render_template('dashboard.html', f_name=f_name, l_name=l_name)
  else:
    return redirect('/login')


@app.route('/create_quiz/<int:id_user>')
def create(id_user):
  if 'id_user' in session and session['id_user'] == id_user:
    return render_template('create_quiz.html', id_user=id_user)
  else:
    return redirect('/login')

@app.route('/save_quiz', methods=['GET', 'POST'])
def save():
  if request.method == 'POST':
    # get the form data
    quiz_name = request.form['quiz_name']
    subject_id = request.form['subject_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    duration = request.form['duration']
    attempts = request.form['attempts']
    # get the number of questions
    num_questions = int(request.form.get('num_questions'))
    # get the questions and options data
    questions = []
    options = []
    for i in range(1, num_questions + 1): # loop for each question
      # get the question content
      question_content = request.form.get('question_{}'.format(i))
      # append it to the questions list
      questions.append(question_content)
      # get the options content and correctness
      option_content = request.form.getlist('option_{}[]'.format(i))
      option_correct = request.form.getlist('correct_option_{}[]'.format(i))
      # zip them together and append them to the options list
      option_data = list(zip(option_content, option_correct))
      options.append(option_data)
    # call the save_quiz function from db module with form data as arguments
    save_quiz(quiz_name, subject_id, start_time, end_time, duration, attempts, num_questions, questions, options)
    # return a response
    return redirect(url_for('/home'))
  else:
    # render the form template
    return render_template('create_quiz.html')




@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)



# from flask import Flask, request, render_template, redirect, session
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# app = Flask(__name__)
# app.secret_key = os.urandom(24)
# db_connection_string = os.environ['DB_CONNECTION_STRING']
# ssl_args = {
#     'ssl': {
#         'ca': '/etc/ssl/cert.pem',
#     }
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': ssl_args}

# db = SQLAlchemy(app)
# class users(db.Model):
#   id = db.Column('user_id', db.Integer, primary_key= True)
#   username = db.Column(db.String(225))
#   user_password = db.Column(db.String(225))  
#   user_role = db.Column(db.Enum('admin', 'student',
#                                  'professor'),
#                          nullable=False)
#   f_name = db.Column(db.String(100))
#   l_name = db.Column(db.String(100))
# def __init__(self, username, user_password,
#              user_role,f_name, l_name):
#   self.username = username
#   self.user_password = user_password
#   self.user_role = user_role
#   self.f_name = f_name
#   self.l_name = l_name



# class Users(db.Model):
#     id = db.Column('user_id', db.Integer, primary_key=True)
#     username = db.Column(db.String(225))
#     user_password = db.Column(db.String(225))
#     user_role = db.Column(db.Enum('admin', 'student', 'professor'), nullable=False)
#     f_name = db.Column(db.String(100))
#     l_name = db.Column(db.String(100))

#     def __init__(self, username, user_password, user_role, f_name, l_name):
#         self.username = username
#         self.user_password = user_password
#         self.user_role = user_role
#         self.f_name = f_name
#         self.l_name = l_name

# def load_users():
#     users = Users.query.all()
#     return users

# data=load_users()

# class Professors(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     degree = db.Column(db.String(255), nullable=False)
#     specialization = db.Column(db.String(255), nullable=False)

#     def __init__(self, degree, specialization):
#         self.degree = degree
#         self.specialization = specialization


# class Students(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, nullable=False)

#     def __init__(self, class_id):
#         self.class_id = class_id


# class Classes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     class_name = db.Column(db.String(255), unique=True, nullable=False)
#     class_field = db.Column(db.String(255), nullable=False)
#     class_level = db.Column(db.Integer, nullable=False)

#     def __init__(self, class_name, class_field, class_level):
#         self.class_name = class_name
#         self.class_field = class_field
#         self.class_level = class_level


# class Subjects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sub_name = db.Column(db.String(255), unique=True, nullable=False)

#     def __init__(self, sub_name):
#         self.sub_name = sub_name


# class ClassSubjects(db.Model):
#     class_id = db.Column(db.Integer, primary_key=True)
#     subject_id = db.Column(db.Integer, primary_key=True)
#     professor_id = db.Column(db.Integer, nullable=False)

#     def __init__(self, class_id, subject_id, professor_id):
#         self.class_id = class_id
#         self.subject_id = subject_id
#         self.professor_id = professor_id


# class Quizzes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_name = db.Column(db.String(255), nullable=False)
#     subject_id = db.Column(db.Integer, nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=False)
#     duration = db.Column(db.Integer, nullable=False)
#     attempts = db.Column(db.Integer, nullable=False)

#     def __init__(self, quiz_name, subject_id, start_time, end_time, duration, attempts):
#         self.quiz_name = quiz_name
#         self.subject_id = subject_id
#         self.start_time = start_time
#         self.end_time = end_time
#         self.duration = duration
#         self.attempts = attempts


# class Questions(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column(db.Integer, nullable=False)
#     q_content = db.Column(db.Text, nullable=False)

#     def __init__(self, quiz_id, q_content):
#         self.quiz_id = quiz_id
#         self.q_content = q_content


# class Options(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, nullable=False)
#     o_content = db.Column(db.Text, nullable=False)
#     is_correct = db.Column(db.Boolean, nullable=False)

#     def __init__(self, question_id, o_content, is_correct):
#         self.question_id = question_id
#         self.o_content = o_content
#         self.is_correct = is_correct


# class QuizResults(db.Model):
#     quiz_id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, primary_key=True)
#     score = db.Column(db.Float, nullable=False)
#     attempt = db.Column(db.Integer, nullable=False)
#     completed_at = db.Column(db.DateTime, nullable=False)

#     def __init__(self, quiz_id, student_id, score, attempt, completed_at):
#         self.quiz_id = quiz_id
#         self.student_id = student_id
#         self.score = score
#         self.attempt = attempt
#         self.completed_at = completed_at


# class StudentAnswers(db.Model):
#     quiz_result_id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, primary_key=True)
#     option_id = db.Column(db.Integer, nullable=False)

#     def __init__(self, quiz_result_id, question_id, option_id):
#         self.quiz_result_id = quiz_result_id
#         self.question_id = question_id
#         self.option_id = option_id

# Routes go here

# @app.route('/')
# def index():
#     if 'username' in session:
#         return redirect('/home/' + str(session['id_user']))
#     else:
#         return redirect('login')


# @app.route('/home')
# def nhome():
#     if 'username' in session:
#         return redirect('/home/' + str(session['id_user']))
#     else:
#         return redirect('login')


# @app.route('/home/')
# def nonhome():
#     if 'username' in session:
#         return redirect('/home/' + str(session['id_user']))
#     else:
#         return redirect('login')



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in session:
#         return redirect('/home/' + str(session['id_user']))
#     else:
#         if request.method == 'POST':
#             username = request.form['username']
#             password = request.form['password']

#             user = Users.query.filter_by(username=username, user_password=password).first()

#             if user:
#                 session['id_user'] = user.id
#                 session['first_name'] = user.f_name
#                 session['last_name'] = user.l_name
#                 session['username'] = user.username
#                 session['user_role'] = user.user_role
#                 return redirect('/home/' + str(session['id_user']))
#             else:
#                 error = 'Invalid username or password. Please try again.'
#                 return render_template('login.html', error=error)

#         return render_template('login.html')



# @app.route('/home')
# def home(id_user):
#     user_role = session.get('user_role')
#     if user_role == 'student':
#         return render_template('st_home.html', session=session)
#     elif user_role == 'professor':
#         return render_template('pr_home.html', session=session)
#     elif user_role == 'admin':
#         f_name = session.get('first_name')
#         l_name = session.get('last_name')
#         return render_template('dashboard.html', f_name=f_name, l_name=l_name)
#     else:
#         return redirect('/login')


# @app.route('/logout')
# def logout():
#   session.clear()
#   return redirect('/login')


# if __name__ == "__main__":
#   app.run(host='0.0.0.0', debug=True)