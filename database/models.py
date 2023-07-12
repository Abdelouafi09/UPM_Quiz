from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String(255), unique=True, nullable=False)
  password = Column(String(255), nullable=False)
  role = Column(Enum('admin', 'student', 'professor'), nullable=False)

  __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': role}


class Professor(User):
  __tablename__ = 'professors'

  user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
  degree = Column(String(255), nullable=False)
  specialization = Column(String(255), nullable=False)

  __mapper_args__ = {'polymorphic_identity': 'professor'}


class Student(User):
  __tablename__ = 'students'

  user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
  class_id = Column(Integer, nullable=False)

  __mapper_args__ = {'polymorphic_identity': 'student'}


class Class(Base):
  __tablename__ = 'classes'

  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True, nullable=False)
  field = Column(String(255), nullable=False)
  level = Column(Integer, nullable=False)


class Subject(Base):
  __tablename__ = 'subjects'

  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True, nullable=False)


class ClassSubject(Base):
  __tablename__ = 'class_subjects'

  class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)
  subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
  professor_id = Column(Integer, ForeignKey('professors.user_id'))


class Quiz(Base):
  __tablename__ = 'quizzes'

  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False)
  subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
  start_time = Column(DateTime, nullable=False)
  end_time = Column(DateTime, nullable=False)
  duration = Column(Integer, nullable=False)
  attempts = Column(Integer, nullable=False)


class Question(Base):
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
  content = Column(Text, nullable=False)

  quiz = relationship('Quiz', backref='questions')


class Option(Base):
  __tablename__ = 'options'

  id = Column(Integer, primary_key=True)
  question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
  content = Column(Text, nullable=False)
  is_correct = Column(Boolean, nullable=False)

  question = relationship('Question', backref='options')


class QuizResult(Base):
  __tablename__ = 'quiz_results'

  quiz_id = Column(Integer, ForeignKey('quizzes.id'), primary_key=True)
  student_id = Column(Integer,
                      ForeignKey('students.user_id'),
                      primary_key=True)
  score = Column(float, nullable=False)
  attempt = Column(Integer, nullable=False)
  completed_at = Column(DateTime, nullable=False)


class StudentAnswer(Base):
  __tablename__ = 'student_answers'

  quiz_result_id = Column(Integer,
                          ForeignKey('quiz_results.quiz_id'),
                          primary_key=True)
  question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
  option_id = Column(Integer, ForeignKey('options.id'))

  quiz_result = relationship('QuizResult', backref='answers')
  question = relationship('Question', backref='student_answers')
  option = relationship('Option')
