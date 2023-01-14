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

# english_text = "I would pay everything I own for a meal there "

response = requests.post("http://127.0.0.1:8000/se", json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/textblob.json", "w"))

english_text['classifier'] = 'vader'

response = requests.post("http://127.0.0.1:8000/se", json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/vader.json", "w"))

del english_text['classifier']
english_text['classifiers'] = ['text_blob', 'vader']

response = requests.post("http://127.0.0.1:8000/se/multiple", json=english_text)

print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/multiple.json", "w"))

response = requests.post("http://127.0.0.1:8000/se/compare", json=english_text)
print(json.dumps(response.json(), indent=4, sort_keys=True), file = open("output/compare.json", "w"))