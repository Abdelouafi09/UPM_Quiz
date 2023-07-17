from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_users():
  with engine.connect() as conn:
    result = conn.execute(text("select * from users"))
    data = result.all()
    keys = ['id_user', 'username', 'password', 'role', 'f_name', 'l_name']
    resultf = [dict(zip(keys, values)) for values in data]
    return (resultf)


def load_subjects_for_professor(professor_id):
    with engine.connect() as conn:
        query = text("""
            SELECT s.id, s.sub_name
            FROM subjects AS s
            JOIN class_subjects AS cs ON s.id = cs.subject_id
            WHERE cs.professor_id = :professor_id
        """).bindparams(professor_id=professor_id)
        result = conn.execute(query)
        subjects = []
        for row in result:
            subject_id, subject_name = row
            subjects.append({'id': subject_id, 'sub_name': subject_name})
        return subjects


