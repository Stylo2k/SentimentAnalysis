import json
import requests


URL = "http://127.0.0.1:8000"


# do a get request to get the names of the available classifiers
available_classifiers = requests.get(URL).json()

print(f'Classifiers: {available_classifiers}')

def get_sentiment(text):
    response = requests.post(f"{URL}/multiple", json={
        'text' : [text],
        'classifiers' : available_classifiers
    })
    return response


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data



data = read_json_file('datasets/Commit Mining/terraform_tf_keywords.json')


text = []

for repo in data.get('repositories'):
    commits = repo.get('commits')
    for commit in commits:
        message = commit.get('msg')
        print(json.dumps(get_sentiment(message).json(), indent=4, sort_keys=True), file=open("commits_analysis.json", "a"))
        
