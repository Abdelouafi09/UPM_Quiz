from flask import Flask, render_template, request, redirect, session
from database.db import load_users

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Set a secret key for session management

# Mock user data (replace with actual user retrieval from the database)
users = load_users()


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
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    # Check if user exists and credentials are valid
    user = next(
      (user for user in users
       if user['username'] == username and user['password'] == password), None)

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


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
