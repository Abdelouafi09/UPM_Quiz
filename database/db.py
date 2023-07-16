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
