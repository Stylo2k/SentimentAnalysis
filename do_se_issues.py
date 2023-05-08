import json
from unittest import skip


import requests


URL = "http://127.0.0.1:8000"


# do a get request to get the names of the available classifiers
available_classifiers = requests.get(URL).json()

print(f'Classifiers: {available_classifiers}')


def debug(string):
    print(f'[DEBUG] {string}')
    exit(0)

def get_sentiment(text):
    if isinstance(text, str):
        text = [text]
    try:
        response = requests.post(f"{URL}/multiple", json={
            'text' : text,
            'classifiers' : available_classifiers
        })
    except Exception as e:
        return {
            [
                {
                    'backend' : 'error',
                }
            ]
        }
    return response



def save_file():
    with open('dataset_issues_sentiment.json', 'w') as f:
        json.dump(issues_data, f, indent=4)


# read json file called dataset_issues.json
issues_data = json.load(open('dataset_issues.json'))


for issue in issues_data:
    body = issue.get('content').get('body')

    issue['sentiment'] = {
        'body' : {},
        'comments' : {}
    }

    if body and any(word in body for word in ['cheap', 'expens', 'cost', 'efficient', 'bill', 'pay']):
        body_sentiment = get_sentiment(body)
        res = body_sentiment.json()[0]
        sea = res.get('sentiment')
        issue['sentiment']['body'] = sea
    else:
        issue['sentiment']['body'] = 'skipped - does not contain any keywords'


    comments = issue.get('content').get('comments')
    
    index = 0
    for comment in comments:
        if comment and any(word in comment for word in ['cheap', 'expens', 'cost', 'efficient', 'bill', 'pay']):
            comment_sentiment = get_sentiment(comment)
            res = comment_sentiment.json()[0]
            sea = res.get('sentiment')
            issue['sentiment']['comments'][index] = sea
        else:
            issue['sentiment']['comments'][index] = 'skipped - does not contain any keywords'
        index += 1

save_file()

