import functools
from datetime import datetime
import codeforces_api
import cx_Oracle
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from codeforces_api import CodeforcesApi
from .db import commit_db, get_db, query_db

bp = Blueprint("home", __name__)

@bp.route('/home')
def home():
    
    cf_handle = g.cf_handle



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
        ''', {'cf_handle': cf_handle})

    print(res)
    
    rating_chart = {
        'label': [],
        'value': []
    }
    for row in res:
        rating_chart['label'].append(row['problem_rating'])
        rating_chart['value'].append(row['num'])
        

    print(rating_chart)

    return render_template("index.html", rating_chart=rating_chart)