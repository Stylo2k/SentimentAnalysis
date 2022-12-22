# File name: model_client.py
import requests


english_text = "The food was allright"

response = requests.post("http://127.0.0.1:3000/", json=english_text)
restext = response.text

print(restext)
