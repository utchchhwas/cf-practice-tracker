from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from cf_tracker.auth import login_required
import cx_Oracle

from .db import commit_db, get_db, query_db


bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route('/<username>', methods=('GET', 'POST'))
# @login_required
def account(username):

    # check if logged in user is the current user
    if username != g.username:
        flash('Please log in first', 'error')
        return redirect(url_for('auth.login'))

    print(f'>> log: showing account page for {username}')

    if request.method == 'POST':
        cf_handle = request.form['cf_handle'].strip().lower()
        password = request.form['password']
        new_password1 = request.form['new_password1']
        new_password2 = request.form['new_password2']

        print(f'>> log: cf_handle = {cf_handle}')
        print(f'>> log: password = {password}')
        print(f'>> log: new_password1 = {new_password1}')
        print(f'>> log: new_password2 = {new_password2}')

        errors = []

        if len(new_password1) > 0 or len(new_password2) > 0:
            if new_password1 != new_password2:
                errors.append('The passwords do not match')

        real_password = query_db('''
            SELECT PASSWORD FROM USERS
            WHERE username = :username
            ''', [username], True)['password']
        if not check_password_hash(real_password, password):
            errors.append(f'Invalid current password')

        print(f'>> log: errors = {errors}')

        if len(errors) == 0:
            current_cf_handle = query_db('''
                SELECT CF_HANDLE FROM USERS
                WHERE USERNAME = :username
                ''', [username], True)['cf_handle']

            if current_cf_handle != cf_handle:
                get_db().execute('''
                    UPDATE USERS
                    SET CF_HANDLE = :cf_handle
                    WHERE USERNAME = :username
                    ''', [cf_handle, username])

                flash('Codeforces handle successfully updated', 'success')
            
            if len(new_password1) > 0:
                get_db().execute('''
                    UPDATE USERS
                    SET PASSWORD = :password
                    WHERE USERNAME = :username
                    ''', [generate_password_hash(new_password1), username])

                flash('Password successfully updated', 'success')

            commit_db()

            return redirect(url_for('account.account', username=g.username))

        else:
            for error in errors:
                flash(error)

    return render_template('account/account.html', username=username)

