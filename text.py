import requests
import json
import time
import os


def get_problem_list():
    start_time = time.time()
    url = 'https://codeforces.com/api/problemset.problems'
    response = requests.get(url)
    end_time = time.time()
    print('Request took {0:.2f}s'.format(end_time - start_time))

    json_obj = json.loads(response.text)
    if json_obj['status'] == 'OK':
        problem_list = json_obj['result']['problems']
        print('Fetched {} {}'.format(len(problem_list),
              'problems' if len(problem_list) > 1 else 'problem'))
        return problem_list
    else:
        raise Exception(json_obj['comment'])


def save_problem_list():
    problem_list = get_problem_list()
    parent_path = 'C:\\Users\\utchchhwas\\OneDrive\\Documents\\Competitive Programming\\CP Automation with Python'
    with open(os.path.join(parent_path, 'problem_list.json'), 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(problem_list, indent=4))


# save_problem_list()
