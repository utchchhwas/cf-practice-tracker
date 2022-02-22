import functools
from datetime import datetime
from tabnanny import check
from turtle import update
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


def insert_or_update_contest_participation(cf_handle):
    
    print(f'>> log: fetching rating change information from codeforces api [cf_handle={cf_handle}]')

    rcs = CodeforcesApi().user_rating(cf_handle)

    print(f'>> log: fetched {len(rcs)} rating changes')


    print(f'>> log: updating CONTEST_PARTICIPATION [cf_handle={cf_handle}]')

    for rc in rcs:

        get_db().execute('''
            MERGE INTO CONTEST_PARTICIPATIONS
            USING dual ON (
                CF_HANDLE = :cf_handle
                AND CONTEST_ID = :contest_id
            )

            WHEN NOT MATCHED THEN 
                INSERT (
                    CF_HANDLE,
                    CONTEST_ID,
                    CONTEST_RANK,
                    OLD_RATING,
                    NEW_RATING
                )
                VALUES (
                    :cf_handle,
                    :contest_id,
                    :contest_rank,
                    :old_rating,
                    :new_rating
                )
            ''',
            {
                'cf_handle': cf_handle,
                'contest_id': rc.contest_id,
                'contest_rank': rc.rank,
                'old_rating': rc.old_rating,
                'new_rating': rc.new_rating
            }
        )
    commit_db()

    print(f'>> log: successfully updated CONTEST_PARTICIPATION [cf_handle={cf_handle}]')


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
            insert_or_update_contest_participation(cf_handle)

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
                flash(error, category='danger')

    return render_template('auth/register.html')


@bp.route("/login", methods=('GET', 'POST'))
def login():

    if request.method == 'POST':

        username = request.form['username'].strip().lower()
        password = request.form['password']

        print(f'>> log: logging in user {username}')

        user = query_db('''
            SELECT * FROM USERS
            WHERE username = :username
            ''', {
                'username': username
            }, fetchone=True)

        print(f'>> log: user={user}')

        errors = []

        if user is None:
            errors.append(f'Invalid username [{username}]')
        elif not check_password_hash(user['password'], password):
            errors.append(f'Invalid password')

        print(f'>> log: errors: {errors}')
        
        if len(errors) == 0:

            print(f'>> log: loggin in user {username}')

            session.clear()  # clear any existing session data
            session['username'] = user['username']  # set username for current session
            session['cf_handle'] = user['cf_handle']  # set cf_handle for current session

            return redirect(url_for('auth.user', username=username))

        else:
            for error in errors:
                flash(error, category='danger')

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
            SELECT CF_HANDLE 
            FROM USERS
            WHERE 
                USERNAME = :username
            ''', {
                'username': username
            }, True)['cf_handle']
        
        print('>> log: loaded username={}, cf_handle={}'.format(g.username, g.cf_handle))


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if g.username is None:
            flash('Please log in first')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view



def check_logged_in_user(username):
    return username == g.username


@bp.route('user/<username>', methods=('GET', 'POST'))
@login_required
def user(username):

    if not check_logged_in_user(username):

        logout()

        flash('Please log in first')

        return redirect(url_for('auth.login'))


    print(f'>> log: showing account page for {username}')

    if request.method == 'POST':

        cf_handle = request.form['cf_handle'].strip().lower()
        password = request.form['password']
        new_password1 = request.form['new_password1']
        new_password2 = request.form['new_password2']

        real_password = query_db('''
            SELECT PASSWORD FROM USERS
            WHERE username = :username
            ''', [username], fetchone=True)['password']


        errors = []

        if not is_valid_cf_handle(cf_handle):
            errors.append(f'Invalid Codeforces handle [{cf_handle}]')

        if len(new_password1) > 0 or len(new_password2) > 0:
            if new_password1 != new_password2:
                errors.append('The passwords do not match')
        
        if not check_password_hash(real_password, password):
            errors.append(f'Invalid current password')


        print(f'>> log: errors = {errors}')

        if len(errors) == 0:

            current_cf_handle = query_db('''
                SELECT CF_HANDLE FROM USERS
                WHERE USERNAME = :username
                ''', [username], True)['cf_handle']

            if current_cf_handle != cf_handle:

                insert_or_update_cf_user(cf_handle)
                insert_or_update_cf_user_submissions(cf_handle)
                insert_or_update_contest_participation(cf_handle)

                get_db().execute('''
                    UPDATE USERS
                    SET CF_HANDLE = :cf_handle
                    WHERE USERNAME = :username
                    ''', [cf_handle, username])
                commit_db()

                flash('Codeforces handle successfully updated')

                g.cf_handle = cf_handle
            
            if len(new_password1) > 0:

                get_db().execute('''
                    UPDATE USERS
                    SET 
                        PASSWORD = :password
                    WHERE 
                        USERNAME = :username
                    ''', {
                        'username': username,
                        'password': generate_password_hash(new_password1)
                    })
                commit_db()

                flash('Password successfully updated', 'success')

        else:
            for error in errors:
                flash(error)

    return render_template('auth/user.html')


@bp.route('/admin/login', methods=('GET', 'POST'))
def admin_login():

    if request.method == 'POST':

        username = request.form['username'].strip().lower()
        password = request.form['password']

        print(f'>> log: logging in admin user {username}')

        user = query_db('''
            SELECT * FROM USERS
            WHERE username = :username
            ''', {
                'username': username
            }, fetchone=True)

        print(f'>> log: user={user}')

        errors = []

        if user is None or user['is_admin'] != 'Y':
            errors.append(f'Invalid admin user [{username}]')
        elif not check_password_hash(user['password'], password):
            errors.append(f'Invalid password')

        print(f'>> log: errors: {errors}')
        
        if len(errors) == 0:

            print(f'>> log: loggin in admin user {username}')

            session.clear()  # clear any existing session data
            session['username'] = user['username']  # set username for current session
            session['admin_username'] = user['username']
            session['cf_handle'] = user['cf_handle']  # set cf_handle for current session

            return redirect(url_for('auth.admin_page', admin_username=username))

        else:
            for error in errors:
                flash(error, category='danger')
    return render_template('auth/admin_login.html')


def check_admin_user(admin_username):

    print(f'>> log: checking admin_username={admin_username}')

    session_admin_username = session.get('admin_username')

    print(f'>> log: session_admin_username={session_admin_username}')

    return session_admin_username is not None and session_admin_username == admin_username



def update_contests():
    
    print(f'>> log: fetching contests information from codeforces api')

    contests = CodeforcesApi().contest_list()

    print(f'>> log: fetched {len(contests)} contests')


    print(f'>> log: updating CONTESTS')

    for contest in contests:

        get_db().execute('''
            MERGE INTO CONTESTS
            USING dual ON (CONTEST_ID = :contest_id)

            WHEN NOT MATCHED THEN 
                INSERT (
                    CONTEST_ID,
                    CONTEST_NAME,
                    START_TIME
                )
                VALUES (
                    :contest_id,
                    :contest_name,
                    TO_DATE(:start_time, 'YYYY-MM-DD HH24:MI:SS')
                )
            ''',
            {
                'contest_id': contest.id,
                'contest_name': contest.name,
                'start_time': str(datetime.fromtimestamp(contest.start_time_seconds))
            }
        )
    commit_db()

    print(f'>> log: successfully updated CONTESTS')



def update_problems():

    print(f'>> log: fetching problems information from codeforces api')

    problems = CodeforcesApi().problemset_problems()['problems']

    print(f'>> log: fetched {len(problems)} problems')


    print(f'>> log: updating PROBLEMS and PROBLEM_TAGS')

    for problem in problems:
        problem: codeforces_api.Problem

        get_db().execute('''
        
            MERGE INTO PROBLEMS
            USING dual ON (
                CONTEST_ID = :contest_id 
                AND PROBLEM_INDEX = :problem_index
            )
            WHEN NOT MATCHED THEN 
                INSERT (
                    CONTEST_ID,
                    PROBLEM_INDEX,
                    PROBLEM_NAME,
                    PROBLEM_RATING
                )
                VALUES (
                    :contest_id,
                    :problem_index,
                    :problem_name,
                    :problem_rating
                )
            ''',
            {
                'contest_id': problem.contest_id,
                'problem_index': problem.index,
                'problem_name': problem.name,
                'problem_rating': problem.rating
            }
        )

        for tag in problem.tags:
            get_db().execute('''
                MERGE INTO PROBLEM_TAGS
                USING dual ON (
                    CONTEST_ID = :contest_id 
                    AND PROBLEM_INDEX = :problem_index
                    AND TAG_NAME = :tag_name
                )
                WHEN NOT MATCHED THEN 
                    INSERT (
                        CONTEST_ID,
                        PROBLEM_INDEX,
                        TAG_NAME
                    )
                    VALUES (
                        :contest_id,
                        :problem_index,
                        :tag_name
                    )
                ''',
                {
                    'contest_id': problem.contest_id,
                    'problem_index': problem.index,
                    'tag_name': tag
                }
            )

    commit_db()

    print(f'>> log: successfully updated PROBLEMS and PROBLEM_TAGS')



@bp.route('/admin_page/<admin_username>', methods=('GET', 'POST'))
def admin_page(admin_username):

    print(f'>> log: showing admin page [admin_username={admin_username}]')

    if not check_admin_user(admin_username):

        logout()

        flash('Please log in as admin')

        return redirect(url_for('auth.admin_login'))


    if request.method == 'POST':

        print(f'>> log: updating database')

        update_contests()
        update_problems()


    return render_template('auth/admin_page.html')

