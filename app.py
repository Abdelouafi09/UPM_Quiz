# from flask import Flask, render_template, request, redirect, session
# from database.db import load_users, load_subjects_for_professor

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# # Set a secret key for session management

# # Mock user data (replace with actual user retrieval from the database)

# @app.route('/')
# def index():
#   if 'username' in session:
#     return redirect('/home/' + str(session['id_user']))
#   else:
#     return redirect('login')

# @app.route('/home')
# def nhome():
#   if 'username' in session:
#     return redirect('/home/' + str(session['id_user']))
#   else:
#     return redirect('login')

# @app.route('/home/')
# def nonhome():
#   if 'username' in session:
#     return redirect('/home/' + str(session['id_user']))
#   else:
#     return redirect('login')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#   if 'username' in session:
#     return redirect('/home/' + str(session['id_user']))
#   else:
#     users = load_users()
#     if request.method == 'POST':
#       username = request.form['username']
#       password = request.form['password']

#       user = next(
#         (user for user in users
#          if user['username'] == username and user['password'] == password),
#         None)
#       if user:
#         session['id_user'] = user['id_user']
#         session['first_name'] = user['f_name']
#         session['last_name'] = user['l_name']
#         session['username'] = user['username']
#         session['user_role'] = user['role']
#         return redirect('/home/' + str(session['id_user']))
#       else:
#         error = 'Invalid username or password. Please try again.'
#         return render_template('login.html', error=error)
#     return render_template('login.html')

# @app.route('/home/<int:id_user>')
# def home(id_user):
#   f_name = session.get('first_name')
#   l_name = session.get('last_name')
#   user_role = session.get('user_role')

#   if user_role == 'student':
#     return render_template('st_home.html', session=session)
#   elif user_role == 'professor':
#     return render_template('pr_home.html', session=session)
#   elif user_role == 'admin':
#     return render_template('dashboard.html', f_name=f_name, l_name=l_name)
#   else:
#     return redirect('/login')

# @app.route('/create_quiz/<int:id_user>')
# def create(id_user):
#   if 'id_user' in session and session['id_user'] == id_user:
#     SUBJECTS = load_subjects_for_professor(id_user)
#     return render_template('create_quiz.html',
#                            id_user=id_user,
#                            subjects=SUBJECTS)
#   else:
#     return redirect('/login')

# @app.route('/logout')
# def logout():
#   session.clear()
#   return redirect('/login')

# if __name__ == "__main__":
#   app.run(host='0.0.0.0', debug=True)

from flask import Flask, request, render_template, redirect, session
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})
Session = sessionmaker(bind=engine)
session0 = Session()
Base = declarative_base()


class User(Base):
  __tablename__ = 'users'
  user_id = Column(Integer, primary_key=True)
  username = Column(String(255), unique=True, nullable=False)
  user_password = Column(String(255), nullable=False)
  user_role = Column(Enum('admin', 'student', 'professor'), nullable=False)
  f_name = Column(String(100), nullable=False)
  l_name = Column(String(100), nullable=False)


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


#   if 'username' in session:
#     return redirect('/home/' + str(session['id_user']))
#   else:
#     users = load_users()
#     if request.method == 'POST':
#       username = request.form['username']
#       password = request.form['password']

#       user = next(
#         (user for user in users
#          if user['username'] == username and user['password'] == password),
#         None)
#       if user:
#         session['id_user'] = user['id_user']
#         session['first_name'] = user['f_name']
#         session['last_name'] = user['l_name']
#         session['username'] = user['username']
#         session['user_role'] = user['role']
#         return redirect('/home/' + str(session['id_user']))
#       else:
#         error = 'Invalid username or password. Please try again.'
#         return render_template('login.html', error=error)
#     return render_template('login.html')

# @app.route('/create_quiz/<int:id_user>')
# def create(id_user):
#   if 'id_user' in session and session['id_user'] == id_user:
#     SUBJECTS = load_subjects_for_professor(id_user)
#     return render_template('create_quiz.html',
#                            id_user=id_user,
#                            subjects=SUBJECTS)
#   else:
#     return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
  username = request.form['username']
  password = request.form['password']
  role = request.form['role']
  f_name = request.form['f_name']
  l_name = request.form['l_name']

  # Create a new user object
  new_user = User(username=username,
                  user_password=password,
                  user_role=role,
                  f_name=f_name,
                  l_name=l_name)

  # Add the new user to the session and commit the changes to the database
  session0.add(new_user)
  session0.commit()

  return 'User added successfully!'


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
