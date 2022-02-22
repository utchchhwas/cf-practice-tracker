from flask import redirect, url_for
from flask import Blueprint, render_template, request

from cf_tracker.db import get_db, query_db

bp = Blueprint("problems", __name__, url_prefix="/problems")

@bp.route("/problems", methods=('GET', 'POST'))
def problems(problem_id=None):

    if request.method == "POST":
        # print("in post method")
        problem_rating_low = request.form["problem_rating_low"]
        problem_rating_high = request.form["problem_rating_high"]
        print(f"problem_rating_low = {problem_rating_low}") 
        print(f"problem_rating_high = {problem_rating_high}")
        if problem_rating_high == "":
            problem_rating_high=4000
        if problem_rating_low == "":
            problem_rating_low=800
        return redirect(url_for("problems.problems", problem_rating_low=problem_rating_low, problem_rating_high=problem_rating_high))

    rating_low = request.args.get("problem_rating_low", 800)
    rating_high = request.args.get("problem_rating_high", 4000)

    print(rating_high)
    print(rating_low)
    all_problems = query_db('''
        SELECT CONTEST_ID, PROBLEM_INDEX, PROBLEM_NAME, PROBLEM_RATING,
            (TO_CHAR(CONTEST_ID) || PROBLEM_INDEX) PROBLEM_ID, 
            ('https://codeforces.com/contest/' || TO_CHAR(CONTEST_ID) || '/problem/' || PROBLEM_INDEX) PROBLEM_LINK
        FROM PROBLEMS
        WHERE PROBLEM_RATING >= :rating_low AND PROBLEM_RATING <= :rating_high
        ORDER BY PROBLEM_RATING
        ''', [rating_low, rating_high])

    return render_template("problems/problems.html", all_problems=all_problems)





