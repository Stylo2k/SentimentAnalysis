# File name: model_client.py
import requests
import json

english_text =  {
 'text' : [
    "The food was allright",
    "The food was great",
    "The food was terrible",
    "The food was amazing",
    "that was the best food I've ever had",
    "I would never eat there again",
    "I would eat there every day if I could",
    "I would pay $100 for a meal there",
],
    'classifier' : 'text_blob'
}

labelled_text = [
    {
        "sentence" : "The food was all right",
        "sentiment" : "neutral"
    },
    {
        "sentence" : "The food was great",
        "sentiment" : "positive"
    },
    {
        "sentence" : "The food was terrible",
        "sentiment" : "negative"
    },
    {
        "sentence" : "The food was amazing",
        "sentiment" : "positive"
    },
    {
        "sentence" : "that was the best food I've ever had",
        "sentiment" : "positive"
    },
    {
        "sentence" : "I would never eat there again",
        "sentiment" : "negative"
    }
]


# english_text = "I would pay everything I own for a meal there "
URL = "http://127.0.0.1:8000"
response = requests.post(URL, json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/text_blob.json", "w"))

english_text['classifier'] = 'vader'

response = requests.post(URL, json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/vader.json", "w"))

english_text['classifier'] = 'stanza'

response = requests.post(URL, json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/stanza.json", "w"))


response = requests.post(f"{URL}/multiple", json={
    'text' : english_text['text'],
    'classifiers' : ['text_blob', 'vader', 'stanza']
})

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/multiple.json", "w"))

response = requests.post(f"{URL}/compare", json={
    'text' : labelled_text,
    'classifiers' : ['text_blob', 'vader', 'stanza']
})
print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/compare.json", "w"))