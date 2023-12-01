import json

data = json.load(open('vanilla_alpaca_7b.json'))
others = json.load(open('dataset_labelled_v7.json'))

index = 0
for d in others:
    if (d['type'] != 'commit'):
        continue
    if d['content']['message'] != data[index]['input']:
        print("We have a huge problem")
        exit(1)
    
    shees = 0
    for idk in d['sentiment_analysis']:
        if idk['classifier'] == 'expected':
            del d['sentiment_analysis'][shees]
        shees += 1
            
    
    d['sentiment_analysis'].append({
        'classifier': 'vanilla_alpaca',
        'sentiment': data[index]['alpaca_output'],
        'reason' : 'none'
    })
    index += 1

json.dump(others, open('dataset_labelled_v8.json', 'w'), indent=4)