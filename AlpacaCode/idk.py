import json
dataset_data = json.load(open("alpaca_dataset.json"))
# make into a dict
dataset_data = {k: v for k, v in enumerate(dataset_data)}
print(dataset_data[0])