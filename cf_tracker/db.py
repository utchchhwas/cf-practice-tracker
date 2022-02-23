import cx_Oracle
from flask import g


# returns the db connection for the current session
def get_db():
    # print(">> log: getting database connection")
    
    if 'db' not in g:
        # print(">> log: creating a new connection")
        g.db = cx_Oracle.connect(user="c##cf", password="cf", encoding="UTF-8")
    return g.db.cursor()


# commit database
def commit_db():
    db = g.get('db', None)
    if db is not None:
        print('>> log: comitting database')
        db.commit()


# closes the db connection for the current session
# the argument e has to be passed for using close_db with app.teardown_appcontext()
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print(">> log: closing database connection")
        db.close()


def init_app(app):
    # register close_db with teardown contest
    app.teardown_appcontext(close_db)


def make_dict_factory(cur):
    col_names = [d[0].lower() for d in cur.description]
    def create_row(*args):
        return dict(zip(col_names, args))
    return create_row


# query the database
def query_db(query, args=[], fetchone=False):
    # print(">> log: executing query", query.strip(), end='\n')
    cur = get_db().execute(query, args)
    cur.rowfactory = make_dict_factory(cur)
    res = cur.fetchone() if fetchone else cur.fetchall()
    cur.close()
    return res
