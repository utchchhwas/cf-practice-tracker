
from flask import Blueprint, render_template, request

from cf_tracker.db import get_db

bp = Blueprint("contests", __name__, url_prefix="/contests")

@bp.route("/")
def contests():
    # if request.method == 'GET':
    #     contestId = request.form['contestId']
    #     contestName = request.form['contestName']

        # cur = get_db().cursor()
        # cur.execute('''
        #         SELECT * FROM CONTESTS
        #         ''')
        # cur.rowfactory = lambda *args: dict()
    return render_template("contests/contests.html")

