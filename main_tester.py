# File name: model_client.py
import requests
import json


text = [
    "The food was allright",
    "The food was great",
    "The food was terrible",
    "The food was amazing",
    "that was the best food I've ever had",
    "I would never eat there again",
    "I would eat there every day if I could",
    "I would pay $100 for a meal there",
]

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


URL = "http://127.0.0.1:8000/"


# do a get request to get the names of the available classifiers
#available_classifiers = requests.get(URL).json()
available_classifiers = 'text_blob'

# do a post request to classify the text for each classifier
for classifier in available_classifiers:
    response = requests.post(URL, json={
        'text' : text,
        'classifier' : 'text_blob'
    })
    #print(json.dumps(response.json(), indent=4, sort_keys=True), file=open(f"output/{classifier}.json", "w"))
    print(response.json())
'''
# now we do the same thing but with a labelled text to /multiple and /compare
response = requests.post(f"{URL}/multiple", json={
    'text' : labelled_text,
    'classifiers' : available_classifiers
})
#print(json.dumps(response.json(), indent=4, sort_keys=True), file=open("output/multiple.json", "w"))

response = requests.post(f"{URL}/compare", json={
    'text' : labelled_text,
    'classifiers' : available_classifiers
})
#print(json.dumps(response.json(), indent=4, sort_keys=True), file=open("output/compare.json", "w"))
'''
