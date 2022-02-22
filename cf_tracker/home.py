import functools
from datetime import datetime
import codeforces_api
import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from codeforces_api import CodeforcesApi
from .db import commit_db, get_db, query_db

bp = Blueprint("home", __name__)


def get_rating_chart(cf_handle):

    res = query_db('''
            SELECT 
                R.PROBLEM_RATING,
                (
                SELECT
                    COUNT(*)
                FROM
                    (
                    SELECT 
                        CONTEST_ID,
                        PROBLEM_INDEX
                    FROM 
                        PROBLEMS
                        INNER JOIN SUBMISSIONS
                        USING (CONTEST_ID, PROBLEM_INDEX)
                    WHERE
                        PROBLEM_RATING = R.PROBLEM_RATING
                        AND CF_HANDLE = :cf_handle
                        AND VERDICT = 'OK'
                    GROUP BY
                        CONTEST_ID,
                        PROBLEM_INDEX
                    )
                ) NUM
            FROM
                ( 
                    SELECT 
                        DISTINCT PROBLEM_RATING 
                    FROM 
                        PROBLEMS 
                    WHERE 
                        PROBLEM_RATING IS NOT NULL 
                ) R
            ORDER BY
                R.PROBLEM_RATING ASC
        ''', [cf_handle])
    
    res: list
    while len(res) > 0 and res[-1]['num'] == 0:
        res.pop()
    
    rating_chart = {
        'labels': [],
        'data': []
    }
    for row in res:
        rating_chart['labels'].append(row['problem_rating'])
        rating_chart['data'].append(row['num'])
        
    print(rating_chart)

    return rating_chart


def get_cf_user(cf_handle):

    return query_db('''
            SELECT 
                *
            FROM
                CF_USERS
            WHERE
                CF_HANDLE = :cf_handle
        ''', [cf_handle], fetchone=True)


def get_total_problems_solved(cf_handle):

    return query_db('''

        SELECT
            COUNT(*) NUM
        FROM
            (
            SELECT	
                DISTINCT S.CONTEST_ID,
                S.PROBLEM_INDEX
            FROM 
                SUBMISSIONS S
            WHERE
                S.CF_HANDLE = :cf_handle
                AND s.VERDICT = 'OK'
                AND EXISTS (
                    SELECT
                        P.CONTEST_ID, P.PROBLEM_INDEX
                    FROM
                        PROBLEMS P
                    WHERE
                        P.CONTEST_ID = S.CONTEST_ID
                        AND P.PROBLEM_INDEX = S.PROBLEM_INDEX
                )
            )
        ''', [cf_handle], fetchone=True)['num']


def get_total_problems_tried(cf_handle):

    return query_db('''
    
        SELECT
            COUNT(*) NUM
        FROM
            (
            SELECT	
                DISTINCT S.CONTEST_ID,
                S.PROBLEM_INDEX
            FROM 
                SUBMISSIONS S
            WHERE
                S.CF_HANDLE = :cf_handle
                AND EXISTS (
                    SELECT
                        P.CONTEST_ID, P.PROBLEM_INDEX
                    FROM
                        PROBLEMS P
                    WHERE
                        P.CONTEST_ID = S.CONTEST_ID
                        AND P.PROBLEM_INDEX = S.PROBLEM_INDEX
                )
            )
        ''', [cf_handle], fetchone=True)['num']



def get_solved_since(cf_handle: str, days: int):

    return query_db('''
        SELECT
            COUNT(*) NUM
        FROM
        (
            SELECT
                DISTINCT CONTEST_ID, PROBLEM_INDEX
            FROM
                SUBMISSIONS
            WHERE
                CF_HANDLE = :cf_handle
                AND VERDICT = 'OK'
                AND CREATION_TIME >= SYSDATE-:days
                AND (CONTEST_ID, PROBLEM_INDEX)  NOT IN (
                    SELECT
                        DISTINCT CONTEST_ID, PROBLEM_INDEX
                    FROM
                        SUBMISSIONS
                    WHERE
                        CF_HANDLE = :cf_handle
                        AND VERDICT = 'OK'
                        AND CREATION_TIME < SYSDATE-:days
                )
        )''', {
            'cf_handle': cf_handle,
            'days': days
        }, fetchone=True)['num']


@bp.route('/home')
def home():
    
    cf_handle = g.cf_handle

    return render_template("index.html", 
                        cf_handle=cf_handle, 
                        cf_user=get_cf_user(cf_handle),
                        total_problems_tried=get_total_problems_tried(cf_handle),
                        total_problems_solved=get_total_problems_solved(cf_handle),
                        solved_last_week=get_solved_since(cf_handle, 30),
                        solved_last_month=get_solved_since(cf_handle, 30),
                        solved_last_year=get_solved_since(cf_handle, 365),
                        rating_chart=get_rating_chart(cf_handle))
