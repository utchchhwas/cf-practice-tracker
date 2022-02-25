from datetime import datetime
from flask import flash, redirect, url_for
import requests
import json
import time
import cx_Oracle

from .db import get_db, commit_db, query_db


def get_contests():
    print('>> log: getting contests')

    start_time = time.time()
    url = 'https://codeforces.com/api/contest.list'
    response = requests.get(url)
    end_time = time.time()

    print('>> log: request took {0:.2f}s'.format(end_time - start_time))

    json_obj = json.loads(response.text)
    if json_obj['status'] == 'OK':
        contests = json_obj['result']

        print(f'>> log: fetched {len(contests)} contests')

        return contests
    else:
        raise Exception(json_obj['comment'])


def update_contests():
    print('>> log: updating contests')

    contests = get_contests()

    added_cnt = 0

    for contest in contests:
        # if contest['startTimeSeconds'] < 0:
        #     continue

        contest_id = contest['id']
        contest_name = contest['name']
        start_time = str(datetime.fromtimestamp(contest['startTimeSeconds']))

        try:
            get_db().execute('''
                INSERT INTO
                CONTESTS (CONTEST_ID, CONTEST_NAME, START_TIME)
                VALUES (:contest_id, :contest_name, TO_DATE(:start_time, 'YYYY-MM-DD HH24:MI:SS'))
            ''', [contest_id, contest_name, start_time])
        except cx_Oracle.IntegrityError:
            pass
        else:
            added_cnt += 1
            # print(f' log: inserted contest_id = {contest_id} into CONTESTS')
    
    commit_db()
    
    print(f'>> log: added {added_cnt} new entries to CONTESTS')

    flash(f'Added {added_cnt} new contests')


def get_problems():
    print('>> log: getting problems')

    start_time = time.time()
    url = 'https://codeforces.com/api/problemset.problems'
    response = requests.get(url)
    end_time = time.time()

    print('>> log: request took {0:.2f}s'.format(end_time - start_time))

    json_obj = json.loads(response.text)
    if json_obj['status'] == 'OK':
        problems = json_obj['result']['problems']

        print(f'>> log: fetched {len(problems)} contests')

        return problems
    else:
        raise Exception(json_obj['comment'])


def update_problems():
    print('>> log: updating problems')

    problems = get_problems()

    added_cnt = 0

    for problem in problems:
        contest_id = problem['contestId']
        problem_index = problem['index']
        problem_name = problem['name']
        problem_rating = problem.get('rating')
        problem_tags = problem.get('tags')

        try:
            get_db().execute('''
                INSERT INTO
                PROBLEMS (CONTEST_ID, PROBLEM_INDEX, PROBLEM_NAME, PROBLEM_RATING)
                VALUES (:contest_id, :problem_index, :problem_name, :problem_rating)
            ''', [contest_id, problem_index, problem_name, problem_rating])
        except cx_Oracle.IntegrityError:
            pass
        else:
            added_cnt += 1
            # print(f' log: inserted contest_id = {contest_id} into CONTESTS')

        for tag_name in problem_tags:
            try:
                get_db().execute('''
                    INSERT INTO
                    PROBLEM_TAGS (CONTEST_ID, PROBLEM_INDEX, TAG_NAME)
                    VALUES (:contest_id, :problem_index, :tag_name)
                ''', [contest_id, problem_index, tag_name])
            except cx_Oracle.IntegrityError:
                pass
    
    commit_db()
    
    print(f'>> log: added {added_cnt} new entries to PROBLEMS')

    flash(f'Added {added_cnt} new problems')
