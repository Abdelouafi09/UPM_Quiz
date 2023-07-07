from flask import Flask, render_template

app = Flask(__name__)
questions = [{
  'text': 'What is the capital of France?',
  'options': ['Paris', 'London', 'Berlin', 'Rome'],
  'type': 'single'
}, {
  'text': 'Which of the following programming languages is object-oriented?',
  'options': ['Java', 'HTML', 'CSS', 'Python'],
  'type': 'single'
}, {
  'text': 'Select all the prime numbers:',
  'options': ['2', '3', '4', '5', '6', '7', '8', '9'],
  'type': 'multiple'
}]


@app.route("/")
def home():
  return render_template('save_quiz.html', questions=questions)


@app.route("/quiz/create")
def create():
  return render_template('create_quiz.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
