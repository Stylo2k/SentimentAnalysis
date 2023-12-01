import json

data = json.load(open("../SentimentAnalysis/dataset_labelled_v4.json"))

# remove all the data points where the input is the same
inputs = []
for d in data:
    inputs.append(d["input"])

unique_inputs = set(inputs)

print(len(inputs))
print(len(unique_inputs))