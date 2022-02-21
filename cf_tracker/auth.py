import functools
import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from .db import commit_db, get_db, query_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    # handle post requests i.e. registration
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        cf_handle = request.form['cf_handle'].strip().lower()
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
            flash('Account registration successful')
            return redirect(url_for('auth.login'))
        else:
            for error in errors:
                flash(error)

    return render_template('auth/register.html')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    # handle post requests i.e. login request
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
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
            return redirect(url_for('account.account', username=username))
        else:
            for error in errors:
                flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    username = session['username']
    print(f'>> log: logging out user {username}')

    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    print(f'>> log: loading logged in user')

    username = session.get('username')
    if username is None:
        g.username = None
    else:
        g.username = session['username']
        g.cf_handle = query_db('''
            SELECT CF_HANDLE FROM USERS
            WHERE USERNAME = :username
            ''', [username], True)['cf_handle']
        
        print('>> log: loaded username={}, cf_handle={}'.format(g.username, g.cf_handle))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

