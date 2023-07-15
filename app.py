from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Mock user data (replace with actual user retrieval from the database)
users = [{
  'username': 'student1',
  'password': 'student1pass',
  'user_role': 'student'
}, {
  'username': 'professor1',
  'password': 'professor1pass',
  'user_role': 'professor'
}, {
  'username': 'admin',
  'password': 'adminpass',
  'user_role': 'admin'
}]


@app.route('/')
def index():
  if 'username' in session:
    return redirect('/home')
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
      session['username'] = user['username']
      session['user_role'] = user['user_role']
      return redirect('/home')
    else:
      error = 'Invalid username or password. Please try again.'
      return render_template('login.html', error=error)

  return render_template('login.html')


@app.route('/home')
def home():
  username = session.get('username')
  user_role = session.get('user_role')

  if user_role == 'student':
    return render_template('st_home.html', name=username)
  elif user_role == 'professor':
    return render_template('pr_home.html')
  elif user_role == 'admin':
    return render_template('dashboard.html')
  else:
    return redirect('/login')


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
