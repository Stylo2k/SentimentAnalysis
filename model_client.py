# File name: model_client.py
import requests


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
restext = response.text

print(restext)
