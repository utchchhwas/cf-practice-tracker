
from flask import Blueprint, render_template, request

from cf_tracker.db import get_db, query_db

bp = Blueprint("problems", __name__, url_prefix="/problems")

@bp.route("/")
def problems(problem_id=None):
    all_problems = query_db('''
        SELECT CONTEST_ID, PROBLEM_INDEX, PROBLEM_NAME, PROBLEM_RATING,
            (TO_CHAR(CONTEST_ID) || PROBLEM_INDEX) PROBLEM_ID, 
            ('https://codeforces.com/contest/' || TO_CHAR(CONTEST_ID) || '/problem/' || PROBLEM_INDEX) PROBLEM_LINK
        FROM PROBLEMS
        ORDER BY PROBLEM_RATING
        ''')

    return render_template("problems/problems.html", all_problems=all_problems[:100])

