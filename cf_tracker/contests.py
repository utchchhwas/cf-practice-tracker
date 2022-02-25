from flask import Blueprint, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
from cf_tracker.db import get_db, query_db

bp = Blueprint("contests", __name__, url_prefix='/contests')

@bp.route("/contests", methods=('GET', 'POST'))
def contests():
    
    if request.method == "POST":

        contest_id = request.form["contest_id"]

        return redirect(url_for("contests.contests", contest_id=contest_id))
        

    contest_id = request.args.get("contest_id")

    if contest_id is None:
        all_contests = query_db('''
            SELECT CONTEST_ID, CONTEST_NAME, START_TIME, ('https://codeforces.com/contest/' || CONTEST_ID) CONTEST_LINK
            FROM CONTESTS
            ORDER BY START_TIME DESC
        ''')
    
    else:
        all_contests = query_db('''
            SELECT CONTEST_ID, CONTEST_NAME, START_TIME, ('https://codeforces.com/contest/' || CONTEST_ID) CONTEST_LINK
            FROM CONTESTS
            WHERE contest_id = :contest_id
            ORDER BY START_TIME DESC
        ''', [contest_id])

    
    page, per_page, offset = get_page_args(
        page_parameter="p", per_page_parameter="pp", pp=25
    )

    pagination = Pagination(
        p=page,
        pp=per_page,
        total=len(all_contests),
        page_parameter="p",
        per_page_parameter="pp",
    )

    return render_template("contests/contests.html", 
                            all_contests=all_contests[offset:offset+per_page], 
                            pagination=pagination)


@bp.route("/contest/<int:contest_id>")
def contest(contest_id):

    contest_problems = query_db('''
                      SELECT *
                      FROM PROBLEMS
                      WHERE CONTEST_ID=:contest_id 
                      ORDER BY PROBLEM_INDEX ASC
    ''', [contest_id])
    print(contest_problems)


    return render_template("contests/contest_problems.html", contest_problems=contest_problems)


