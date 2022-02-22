from multiprocessing import Condition
from tkinter.tix import Select
from flask import Blueprint, redirect, render_template, request, url_for

from cf_tracker.db import get_db, query_db

bp = Blueprint("contests", __name__, url_prefix="/contests")

@bp.route("/show_contests", methods=('GET', 'POST'))
def show_contests():
    if request.method == "POST":
        # print("in post method")
        contest_id = request.form["contest_id"]
        print(f"contest_id = {contest_id}") 
        return redirect(url_for("contests.show_contests", contest_id=contest_id))
        
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

    return render_template("contests/contests.html", all_contests=all_contests[:100])

@bp.route("/contest/<int:contest_id>")
def contest(contest_id):
    contest_problems = query_db('''
                      SELECT PROBLEM_INDEX, PROBLEM_NAME, PROBLEM_RATING
                      FROM PROBLEMS
                      WHERE CONTEST_ID=:contest_id 
                      ORDER BY PROBLEM_INDEX ASC
    ''', [contest_id])
    print(contest_problems)
    # return f"contest_id = {contest_id}"
    return render_template("contests/contest_problems.html", contest_problems=contest_problems)


