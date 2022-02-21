import functools
from datetime import datetime
import codeforces_api
import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from codeforces_api import CodeforcesApi
from .db import commit_db, get_db, query_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def insert_or_update_cf_user(cf_handle):

    print(f'>> log: fetching user information from codeforces api [cf_handle={cf_handle}]')

    user = CodeforcesApi().user_info([cf_handle])[0]

    print(f'>> log: fetched result = {user.__dict__}')


    print(f'>> log: updating CF_USERS [cf_handle={cf_handle}]')
    
    get_db().execute('''
        MERGE INTO CF_USERS
        USING dual ON (CF_HANDLE = :cf_handle)
        WHEN MATCHED THEN 
            UPDATE SET
                FIRST_NAME = :first_name,
                LAST_NAME = :last_name,
                RATING = :rating,
                MAX_RATING = :max_rating,
                RANK = :rank,
                MAX_RANK = :max_rank,
                TITLE_PHOTO_URL = :title_photo_url,
                COUNTRY = :country
        WHEN NOT MATCHED THEN 
            INSERT (
                CF_HANDLE,
                FIRST_NAME,
                LAST_NAME,
                RATING,
                MAX_RATING,
                RANK,
                MAX_RANK,
                TITLE_PHOTO_URL,
                COUNTRY
            )
            VALUES (
                :cf_handle,
                :first_name,
                :last_name,
                :rating,
                :max_rating,
                :rank,
                :max_rank,
                :title_photo_url,
                :country
            )
        ''',
        {
            "cf_handle": cf_handle,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "rating": user.rating,
            "max_rating": user.max_rating,
            "rank": user.rank,
            "max_rank": user.max_rank,
            "title_photo_url": user.title_photo,
            "country": user.country
        }
    )
    commit_db()

    print(f'>> log: successfully updated CF_USERS [cf_handle={cf_handle}]')


def insert_or_update_cf_user_submissions(cf_handle):
    
    print(f'>> log: fetching submissions information from codeforces api [cf_handle={cf_handle}]')

    subs = CodeforcesApi().user_status(cf_handle)

    print(f'>> log: fetched {len(subs)} submissions')


    print(f'>> log: updating SUBMISSIONS [cf_handle={cf_handle}]')

    for sub in subs:
        sub: codeforces_api.Submission

        get_db().execute('''
            MERGE INTO SUBMISSIONS
            USING dual ON (SUBMISSION_ID = :submission_id)

            WHEN NOT MATCHED THEN 
                INSERT (
                    SUBMISSION_ID,
                    CF_HANDLE,
                    CONTEST_ID,
                    PROBLEM_INDEX,
                    CREATION_TIME,
                    PROGRAMMING_LANG,
                    VERDICT
                )
                VALUES (
                    :submission_id,
                    :cf_handle,
                    :contest_id,
                    :problem_index,
                    TO_DATE(:creation_time, 'YYYY-MM-DD HH24:MI:SS'),
                    :programming_lang,
                    :verdict
                )
            ''',
            {
                'submission_id': sub.id,
                'cf_handle': cf_handle,
                'contest_id': sub.contest_id,
                'problem_index': sub.problem.index,
                'creation_time': str(datetime.fromtimestamp(sub.creation_time_seconds)),
                'programming_lang': sub.programming_language,
                'verdict': sub.verdict
            }
        )
    commit_db()

    print(f'>> log: successfully updated SUBMISSIONS [cf_handle={cf_handle}]')


def insert_user(user: dict):

    print(f'>> log: inserting user={user["username"]} into USERS')

    get_db().execute('''
        INSERT INTO
        USERS (USERNAME, PASSWORD, CF_HANDLE)
        VALUES (:username, :password, :cf_handle)
    ''', user)
    commit_db()

    print(f'>> log: successfully inserted user={user["username"]} into USERS')


def check_user(username):

    res = query_db('''
            SELECT COUNT(*) AS CNT
            FROM USERS
            WHERE 
                USERNAME = :username
        ''', {
            'username': username
        }, fetchone=True)

    return res['cnt'] == 1
    

def is_valid_cf_handle(cf_handle):
    try:
        CodeforcesApi().user_info([cf_handle])
    except:
        return False
    else:
        return True


@bp.route("/register", methods=('GET', 'POST'))
def register():

    if request.method == 'POST':

        username = request.form['username'].strip().lower()
        cf_handle = request.form['cf_handle'].strip().lower()
        password = request.form['password']
        password_confirm = request.form['passwordConfirm']

        print(f'>> log: registering user {username}')

        errors = []

        if check_user(username):
            errors.append(f'User [{username}] already exists')

        if not is_valid_cf_handle(cf_handle):
            errors.append(f'Invalid Codeforces handle [{cf_handle}]')

        if password != password_confirm:
            errors.append('The passwords do not match')
        # elif len(password) < 8:
        #     errors.append('Password must be 8 characters long')

        print(f'>> log: errors={errors}')

        if len(errors) == 0:

            print(f'>> log: registering user={username}')

            insert_or_update_cf_user(cf_handle)
            insert_or_update_cf_user_submissions(cf_handle)

            insert_user({
                'username': username,
                'password': generate_password_hash(password),
                'cf_handle': cf_handle
            })

            print(f'>> log: successfully registered user={username}')

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

