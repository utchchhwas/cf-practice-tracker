import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db, query_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['passwordConfirm']

        if password != password_confirm:
            flash('Passwords do not match', 'error')
        else:
            try:
                get_db().cursor().execute('''
                    INSERT INTO USERS (USERNAME, PASSWORD)
                    VALUES (:username, :password)
                    ''', [username, generate_password_hash(password)])
                get_db().commit()
            except get_db().IntegrityError:
                print(f'Error: Username: {username} already taken')
            else:
                print(f'Log: {username} successfully registered')
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # cur = get_db().cursor()
        # cur.execute('''
        #     SELECT * FROM USERS
        #     WHERE username = :username
        #     ''', [username])
        # cur.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cur.description], args))
        # user = cur.fetchone()
        user = query_db('''
            SELECT * FROM USERS
            WHERE username = :username
            ''', [username], True)
        print(user)

        if user is None:
            print(f'Error: Invalid username')
        elif not check_password_hash(user['password'], password):
            print(f'Error: Invalid password')
        else:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('index'))

    return render_template('auth/login.html')
