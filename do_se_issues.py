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





# read json file called dataset_issues.json
issues_data = json.load(open('dataset_issues.json'))
labeled_issues = json.load(open('dataset_issues_sentiment.json'))

def save_file():
    with open('dataset_issues_sentiment_v2.json', 'w') as f:
        json.dump(labeled_issues, f, indent=4)

def do_sentiment_analysis():
    issue_index = 0
    for issue in issues_data:
        body = issue.get('content').get('body')
        labeled = labeled_issues[issue_index]

        issue['sentiment'] = {
            'body' : {},
            'comments' : {}
        }

        if body and any(word in body for word in ['cheap', 'expens', 'cost', 'efficient', 'bill', 'pay']):
            body_sentiment = get_sentiment(body)
            res = body_sentiment.json()[0]
            sea = res.get('sentiment')
            issue['sentiment']['body'] = labeled['sentiment']['body'] | sea
        else:
            issue['sentiment']['body'] = 'skipped - does not contain any keywords'


        comments = issue.get('content').get('comments')
        
        index = 0
        for comment in comments:
            if comment and any(word in comment for word in ['cheap', 'expens', 'cost', 'efficient', 'bill', 'pay']):
                comment_sentiment = get_sentiment(comment)
                res = comment_sentiment.json()[0]
                sea = res.get('sentiment')
                issue['sentiment']['comments'][index] = labeled['sentiment']['comments'][f'{index}'] | sea
            else:
                issue['sentiment']['comments'][index] = 'skipped - does not contain any keywords'
            index += 1
        
        issue_index += 1
    save_file()

def fix_dataset():
    for issue in labeled_issues:
        if issue.get('sentiment').get('body') != 'skipped - does not contain any keywords':
            text_blob = issue.get('sentiment').get('body').get('text_blob').lower()
            vader = issue.get('sentiment').get('body').get('vader').lower()
            stanza = issue.get('sentiment').get('body').get('stanza').lower()

            gpt = issue.get('sentiment').get('body').get('gpt')
            gpt = gpt.replace('\n', '')
            gpt = gpt.replace('reason:', '"reason":')
            gpt = gpt.replace('Reason:', '"reason":')
            gpt = gpt.replace('"Reason":', '"reason":')
            gpt = gpt.replace('"Sentiment":', '"sentiment":')
            # remove newline characters
        
            gpt = json.loads(gpt)

            gpt['sentiment'] = gpt.get('sentiment').lower()
            reason_none = 'none'

            data_dict = [
                {
                    'classifier' : 'text_blob',
                    'sentiment' : text_blob,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'vader',
                    'sentiment' : vader,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'stanza',
                    'sentiment' : stanza,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'gpt',
                    'sentiment' : gpt.get('sentiment'),
                    'reason' : gpt.get('reason')
                }
            ]

            issue['sentiment']['body'] = data_dict

        comments = issue.get('sentiment').get('comments')
        index = 0
        for comment in comments:
            comment = comments.get(f'{index}')
            
            if comment == 'skipped - does not contain any keywords':
                index += 1
                continue

            text_blob = comment.get('text_blob').lower()
            vader = comment.get('vader').lower()
            stanza = comment.get('stanza').lower()
            
            gpt = comment.get('gpt')
            gpt = gpt.replace('\n', '')
            gpt = gpt.replace('reason:', '"reason":')
            gpt = gpt.replace('Reason:', '"reason":')
            gpt = gpt.replace('"Reason":', '"reason":')
            gpt = gpt.replace('"Sentiment":', '"sentiment":')
            print(gpt)
            gpt = json.loads(gpt)

            gpt['sentiment'] = gpt.get('sentiment').lower()
            reason_none = 'none'

            data_dict_2 = [
                {
                    'classifier' : 'text_blob',
                    'sentiment' : text_blob,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'vader',
                    'sentiment' : vader,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'stanza',
                    'sentiment' : stanza,
                    'reason' : reason_none
                },
                {
                    'classifier' : 'gpt',
                    'sentiment' : gpt.get('sentiment'),
                    'reason' : gpt.get('reason')
                }
            ]

            issue['sentiment']['comments'][f'{index}'] = data_dict_2
            index += 1
        save_file()


if __name__ == "__main__":
    # do_sentiment_analysis()
    fix_dataset()