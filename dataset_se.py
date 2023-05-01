import json
import requests


URL = "http://127.0.0.1:8000"


# do a get request to get the names of the available classifiers
available_classifiers = requests.get(URL).json()

print(f'Classifiers: {available_classifiers}')

wanted_classifiers = 'gpt'

available_classifiers = wanted_classifiers


def get_sentiment(text):
    if isinstance(text, str):
        text = [text]
    response = requests.post(f"{URL}/multiple", json={
        'text' : text,
        'classifiers' : available_classifiers
    })
    return response


def get_one_sentiment(text):
    if isinstance(text, str):
        text = [text]
    response = requests.post(f"{URL}/", json={
        'text' : text,
        'classifier' : available_classifiers
    })
    return response


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data



# data = read_json_file('datasets/Commit Mining/terraform_tf_keywords.json')
data = read_json_file(f'dataset_labelled.json')

all_text = []

        
for element in data:
    text = element.get('content').get('message')
    if not text:
        print(f'issue found, ignoring for now')
        continue
    all_text.append(text)


index = 0

response = get_one_sentiment(all_text).json()


for res in response:
    sentiment = res.get('sentiment')
    data[index]['sentiment']['gpt'] = sentiment
    index += 1


with open('dataset_labelled_v2.json', 'w') as f:
    json.dump(data, f, indent=4)

