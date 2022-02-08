import cx_Oracle
from flask import g


# returns the db connection for the current session
def get_db():
    if 'db' not in g:
        print("Log: Getting database connection")
        g.db = cx_Oracle.connect(user="c##cf", password="cf", encoding="UTF-8")
    return g.db


# closes the db connection for the current session
# the argument e has to be passed for using close_db with app.teardown_appcontext()
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        print("Log: Closing database connection")
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
