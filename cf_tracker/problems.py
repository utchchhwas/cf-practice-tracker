import codeforces_api
from flask import flash, redirect, url_for
from flask import Markup
from flask import Blueprint, render_template, request, g
from cf_tracker.contests import contest
from .auth import check_logged_in_user
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

from cf_tracker.db import get_db, query_db, commit_db

bp = Blueprint("problems", __name__, url_prefix="")

@bp.route("/problems", methods=('GET', 'POST'))
def problems():

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

    return render_template("problems/problems.html", all_problems=all_problems[:10])


def get_problem(contest_id, problem_index):

    return query_db('''
            SELECT *
            FROM PROBLEMS
            WHERE
                CONTEST_ID = :contest_id
                AND PROBLEM_INDEX = :problem_index
        ''', [contest_id, problem_index], fetchone=True)


def get_contest(contest_id):

    return query_db('''
            SELECT *
            FROM CONTESTS
            WHERE
                CONTEST_ID = :contest_id
        ''', [contest_id], fetchone=True)


def get_problem_log(username, contest_id, problem_index):

    return query_db('''
            SELECT
                * 
            FROM
                PROBLEM_LOGS 
            WHERE
                USERNAME = :username
                AND CONTEST_ID = :contest_id
                AND PROBLEM_INDEX = :problem_index
        ''', [username, contest_id, problem_index], fetchone=True)


def get_problem_tags(contest_id, problem_index):

    res = query_db('''
            SELECT TAG_NAME
            FROM PROBLEM_TAGS
            WHERE
                CONTEST_ID = :contest_id
                AND PROBLEM_INDEX = :problem_index
            ORDER BY
                TAG_NAME ASC
        ''', [contest_id, problem_index])

    return [row['tag_name'] for row in  res]


def is_solved(cf_handle, contest_id, problem_index):

    num = query_db('''
        SELECT COUNT(*) NUM
        FROM SUBMISSIONS
        WHERE
            CF_HANDLE = :cf_handle
            AND CONTEST_ID = :contest_id
            AND PROBLEM_INDEX = :problem_index
            AND VERDICT = 'OK'
    ''', [cf_handle, contest_id, problem_index], fetchone=True)['num']

    return num > 0


def get_problem_submissions(cf_handle, contest_id, problem_index):

    return query_db('''
            SELECT *
            FROM SUBMISSIONS
            WHERE
                CF_HANDLE = :cf_handle
                AND CONTEST_ID = :contest_id
                AND PROBLEM_INDEX = :problem_index
            ORDER BY
                CREATION_TIME DESC
        ''', [cf_handle, contest_id, problem_index])



def insert_or_update_problem_logs(username, contest_id, problem_index, personal_comment, todo):
    
    print(f'>> log: updating PROBLEM_LOGS PERSONAL_COMMENT [username={username}], contest_id={contest_id}, problem_index={problem_index}')

    get_db().execute('''
        MERGE INTO PROBLEM_LOGS
        USING dual ON (
            USERNAME = :username
            AND CONTEST_ID = :contest_id
            AND PROBLEM_INDEX = :problem_index    
        )
        WHEN MATCHED THEN 
            UPDATE SET
                PERSONAL_COMMENT = :personal_comment,
                PROBLEM_STATUS = :todo
        WHEN NOT MATCHED THEN 
            INSERT (
                USERNAME,
                CONTEST_ID,
                PROBLEM_INDEX,
                PERSONAL_COMMENT,
                PROBLEM_STATUS
            )
            VALUES (
                :username,
                :contest_id,
                :problem_index,
                :personal_comment,
                :todo
            )
        ''',
        {
            'username': username,
            'contest_id': contest_id,
            'problem_index': problem_index,
            'personal_comment': personal_comment,
            'todo': todo
        }
    )
    commit_db()

    print(f'>> log: successfully updated PROBLEMS_LOG PERSONAL_COMMENT [username={username}, contest_id={contest_id}, problem_index={problem_index}]')


@bp.route('/problem/<int:contest_id>/<problem_index>', methods=('GET', 'POST'))
def problem(contest_id, problem_index):

    username = g.username
    cf_handle = g.cf_handle




    print(f'>> log: in problem page [contest_id={contest_id}, problem_index={problem_index}]')

    problem: codeforces_api.Problem = get_problem(contest_id, problem_index)

    print(f'>> log: problem={problem}')

    if problem is None:

        flash('Invalid problem specification', category='danger')

        return redirect(url_for('problems.problems'))


    if request.method == 'POST':

        print(f'>> log: processing post request in problem page')

        personal_comment = request.form.get('personal_comment', '')

        print(f'>> log: personal_comment={personal_comment}')

        todo = request.form.get('todo')

        print(f'>> log: todo={todo}')

        insert_or_update_problem_logs(username, contest_id, problem_index, personal_comment, todo)


 
    tags = get_problem_tags(contest_id, problem_index)

    print(f'>> log: tags={tags}')


    contest = get_contest(contest_id)

    print(f'>> log: contest={contest}')


    problem_log = get_problem_log(username, contest_id, problem_index)

    print(f'>> log: problem_log={problem_log}')
    
    personal_comment = ''
    if problem_log is not None and problem_log['personal_comment'] is not None:
        personal_comment = problem_log['personal_comment']

    print(f'>> log: personal_comment={personal_comment}')

    todo = None
    if problem_log is not None:
        todo = problem_log['problem_status']


#     submissions = get_problem_submissions(cf_handle, contest_id, problem_index)
# 
#     print(f'>> log: submissions={submissions}')


    solved = is_solved(cf_handle, contest_id, problem_index)

    solved = 'Solved' if solved == True else 'Unsolved'

    print(f'>> log: solved={solved}')


    problem_link = f'https://codeforces.com/contest/{contest_id}/problem/{problem_index}'


    return render_template('problems/problem.html', 
                            contest_id=contest_id,
                            problem_index=problem_index,
                            problem=problem,
                            contest=contest,
                            problem_link=problem_link,
                            solved=solved,
                            tags=tags,
                            personal_comment=personal_comment,
                            todo=todo,
                            )



def get_problem_discussions(contest_id, problem_index):

    print(f'>> log: getting discussions for contest_id={contest_id}, problem_index={problem_index}')

    return query_db('''
            SELECT 
                D.ID,
                D.AUTHOR,
                D.LAST_UPDATE_TIME,
                D.CONTENT,
                (
                    SELECT COUNT(*)
                    FROM PROBLEM_DISCUSSIONS_UP_VOTES
                    WHERE ID = D.ID
                ) UP_VOTES
            FROM PROBLEM_DISCUSSIONS D
            WHERE
                D.CONTEST_ID = :contest_id
                AND D.PROBLEM_INDEX = :problem_index
            ORDER BY
                UP_VOTES DESC,
                D.ID DESC
        ''', [contest_id, problem_index])


@bp.route('/discussion/<int:contest_id>/<problem_index>')
def discussion(contest_id, problem_index):

    print(f'>> log: showing discussion page for contest_id={contest_id}, problem_index={problem}')


    dis = get_problem_discussions(contest_id, problem_index)

    print(f'>> log: discussions={dis}')

    for d in dis:
        content = str(d['content'])
        content = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        content = Markup(content)
        d['content'] = content
        print(f'>> log: content={d["content"]}')


    return render_template('problems/discussions.html', contest_id=contest_id, problem_index=problem_index, dis=dis)


def insert_discussion(username, contest_id, problem_index, content):

    get_db().execute('''
        INSERT INTO 
        PROBLEM_DISCUSSIONS (
            AUTHOR,
            CONTEST_ID,
            PROBLEM_INDEX,
            CONTENT
        )
        VALUES (
            :author,
            :contest_id,
            :problem_index,
            :content
        )
    ''', [username, contest_id, problem_index, content])
    commit_db()



@bp.route('/new_discussion/<username>/<int:contest_id>/<problem_index>', methods=('GET', 'POST'))
def new_discussion(username, contest_id, problem_index):

    print(f'>> log: showing new discussion page for username={username} contest_id={contest_id}, problem_index={problem_index}')

    if not check_logged_in_user(username):

        flash(f'User [{username}] is not logged in')

        return redirect(url_for('problems.problems'))


    if request.method == 'POST':

        print(f'>> log: handing post request in new_discussions')

        content = request.form['content']

        if content != '':

            print(f'>> log: content={content}')

            insert_discussion(username, contest_id, problem_index, content)

            flash('New discussion successfully created', 'success')

        return redirect(url_for('problems.discussion', contest_id=contest_id, problem_index=problem_index))



    return render_template('problems/new_discussion.html', contest_id=contest_id, problem_index=problem_index)



def get_discussion(id):

    return query_db('''
        SELECT *
        FROM PROBLEM_DISCUSSIONS
        WHERE
            ID = :id
        ''', [id], fetchone=True)


def update_discussion(id, content):

    get_db().execute('''
        UPDATE PROBLEM_DISCUSSIONS
        SET
            CONTENT = :content,
            LAST_UPDATE_TIME = SYSDATE
        WHERE
            ID = :id
    ''', {
        'id': id,
        'content': content
    })
    commit_db()


@bp.route('/edit_discussion/<username>/<int:contest_id>/<problem_index>/<id>', methods=('GET', 'POST'))
def edit_discussion(username, contest_id, problem_index, id):

    print(f'>> log: showing edit discussion page for username={username} contest_id={contest_id}, problem_index={problem_index}, id={id}')

    if not check_logged_in_user(username):

        flash(f'User [{username}] is not logged in')

        return redirect(url_for('problems.problems'))


    if request.method == 'POST':

        print(f'>> log: handling post request in edit_discussion')

        content = request.form['content']

        if content != '':
            update_discussion(id, content)

            flash('Discussion successfully updated', 'success')

        return redirect(url_for('problems.discussion', contest_id=contest_id, problem_index=problem_index))


    dis = get_discussion(id)

    print(f'>> log: dis={dis}')

    content = dis['content']

    print(f'>> log: content={content}')
    

    return render_template('problems/edit_discussion.html', id=id, contest_id=contest_id, problem_index=problem_index, content=content)



@bp.route('/up_vote_discussion/<username>/<int:id>')
def up_vote_discussion(username, id):

    print(f'>> log: up voting username={username}, id={id}')

    if not check_logged_in_user(username):

        flash(f'User [{username}] is not logged in')

        return redirect(url_for('problems.problems'))


    contest_id = request.args.get('contest_id')
    problem_index = request.args.get('problem_index')

    get_db().execute('''
        MERGE INTO PROBLEM_DISCUSSIONS_UP_VOTES
        USING dual ON (
            ID = :id
            AND USERNAME = :username
        )
        WHEN NOT MATCHED THEN 
            INSERT (
                ID,
                USERNAME
            )
            VALUES (
                :id,
                :username
            )
        ''',
        {
            'id': id,
            'username': username
        }
    )
    commit_db()

    flash('Discussion up voted', 'success')

    return redirect(url_for('problems.discussion', contest_id=contest_id, problem_index=problem_index))










