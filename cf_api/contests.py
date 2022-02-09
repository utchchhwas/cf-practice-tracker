from datetime import datetime
import requests
import json
import time


def get_contests():
    print('>> log: getting contests')
    start_time = time.time()
    url = 'https://codeforces.com/api/contest.list'
    response = requests.get(url)
    end_time = time.time()
    print(f'>> log: request took {0:.2f}s'.format(end_time - start_time))

    json_obj = json.loads(response.text)
    if json_obj['status'] == 'OK':
        contest_list = json_obj['result']
        print(f'>> log: fetched {len(contests)} contests')
        return contest_list
    else:
        raise Exception(json_obj['comment'])


contests = get_contests()

for contest in contests[10:15]:
    print(contest)
    print(datetime.fromtimestamp(contest['startTimeSeconds']))



