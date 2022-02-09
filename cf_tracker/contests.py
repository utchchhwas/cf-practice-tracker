
from flask import Blueprint, render_template, request

from cf_tracker.db import get_db, query_db

bp = Blueprint("contests", __name__, url_prefix="/contests")

@bp.route("/")
@bp.route("/<contest_id>")
def contests(contest_id=None):
    all_contests = query_db('''
        SELECT CONTEST_ID, CONTEST_NAME, START_TIME, ('https://codeforces.com/contest/' || CONTEST_ID) CONTEST_LINK
        FROM CONTESTS
        ORDER BY START_TIME DESC
    ''')

    return render_template("contests/contests.html", all_contests=all_contests)


