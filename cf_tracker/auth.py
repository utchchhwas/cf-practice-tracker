from distutils.log import error
import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from .db import commit_db, get_db, query_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    # handle post requests i.e. registration
    if request.method == 'POST':
        username = request.form['username'].lower()
        cf_handle = request.form['cf_handle'].lower()
        password = request.form['password']
        password_confirm = request.form['passwordConfirm']

        print(f'>> log: registering user {username}')

        errors = []
        # check for errors
        if password != password_confirm:
            errors.append('The passwords do not match')
        else:
            try:
                get_db().execute('''
                    INSERT INTO USERS (USERNAME, PASSWORD, CF_HANDLE)
                    VALUES (:username, :password, :cf_handle)
                ''', [username, generate_password_hash(password), cf_handle])
                commit_db()

                print(f'>> log: inserted {username} into USERS')
            except cx_Oracle.IntegrityError:
                errors.append(f'{username} is already taken')

        print(f'>> log: errors: {errors}')

        # redirect to login page if no error
        if len(errors) == 0:
            print(f'>> log: user {username} successfully registered')
            return redirect(url_for('auth.login'))
        else:
            for error in errors:
                flash(error)

    return render_template('auth/register.html')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    # handle post requests i.e. login request
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        print(f'>> log: logging in user {username}')

        user = query_db('''
            SELECT * FROM USERS
            WHERE username = :username
            ''', [username], True)

        print(f'>> log: user details: {user}')

        errors = []
        # check for errors
        if user is None:
            errors.append(f'Invalid username: {username}')
        elif not check_password_hash(user['password'], password):
            errors.append(f'Invalid password')

        print(f'>> log: errors: {errors}')
        
        # log in user if no error
        if len(errors) == 0:
            print(f'>> log: loggin in user {username}')
            session.clear()  # clear any existing session data
            session['username'] = user['username']  # set username for current session
            session['cf_handle'] = user['cf_handle']  # set cf_handle for current session
            return redirect(url_for('index'))
        else:
            for error in errors:
                flash(error)

    return render_template('auth/login.html')
