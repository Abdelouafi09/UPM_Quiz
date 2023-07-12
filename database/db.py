from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL database credentials
DB_NAME = "upm_quiz"
DB_USERNAME = "x2d0n4hu08a86335jr05"
DB_PASSWORD = "pscale_pw_jOpQNKgMzzSN5vc7NMoGQ0MjbgPySyE9AdT2cli0Xdj"
DB_HOST = "aws.connect.psdb.cloud"

# Create the database connection URL
DB_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create the engine and session
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
