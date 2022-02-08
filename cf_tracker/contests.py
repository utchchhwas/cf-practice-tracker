
from flask import Blueprint, render_template, request

from cf_tracker.db import get_db, query_db

bp = Blueprint("contests", __name__, url_prefix="/contests")

@bp.route("/")
@bp.route("/<contest_id>")
def contests(contest_id=None):
    print("in contest")
    all_contests = query_db('''
        SELECT * FROM CONTESTS
    ''')
    print(all_contests)
    print(contest_id)
    return render_template("contests/contests.html", all_contests=all_contests)


