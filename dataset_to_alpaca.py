import json

def die(message):
    print(message)
    exit(0)

one_element = {
    "instruction": "What is the sentiment of the following sentence?",
    "input" : None,
    "output" : None,
}


# read the json file called dataset_labelled_v4.json
old_dataset = json.load(open('dataset_labelled_v4.json'))

uni_urls = []
dataset = []
# remove all the elements that have the same url
for element in old_dataset:
    url = element['url']
    if url not in uni_urls:
        uni_urls.append(url)
        dataset.append(element)
    else:
        pass

json.dump(dataset, open('dataset_labelled_v5.json', 'w'), indent=4)
exit(0)
for element in dataset:
    ses = element['sentiment_analysis']
    for se in ses:
        if se['classifier'] == 'alshakoush':
            del element['sentiment_analysis']
            element['sentiment_analysis'] = se
            break

   

alpaca_dataset = [
    {
    "instruction": "What is the sentiment of the following sentence?",
    "input" : element['content']['message'],
    "output" : element['sentiment_analysis']['sentiment'],
    }
    for element in dataset
]

# dump the dataset to a json file called alpaca_dataset.json
json.dump(alpaca_dataset, open('alpaca_dataset_v2.json', 'w'), indent=4)
