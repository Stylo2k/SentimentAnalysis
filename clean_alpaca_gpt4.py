import json

data = json.load(open('alpaca-gpt4.json'))

cleaned = []
dest = json.load(open('alpaca-gpt4-cleaned.json'))


polarities = ['neutral', 'positive', 'negative']

def find_sentiment(sentence):
    # make sentence lowercase
    lower_case = sentence.lower()
    # find neutral, positive, and negative words in the sentence
    indices = [
        lower_case.find(polarity) for polarity in polarities
    ]
    
    manual_override = None
    
    # if more than one of the indices is not -1, then we have a problem
    if (indices.count(-1) == 3):
        print(f"could not find any for {sentence}")
        # get manual override from the user
        manual_override = input("manual override: ")
    elif (indices.count(-1) < 2):
        # choose the one with the lowest index
        return polarities[indices.index(min(indices))], min(indices)
        
    
    if manual_override:
        return manual_override, -1
        
    
    if indices[0] != -1:
        return 'neutral', indices[0]
    elif indices[1] != -1:
        return 'positive', indices[1]
    elif indices[2] != -1:
        return 'negative', indices[2]
            
    

for d in data:
    sentiment, index = find_sentiment(d['alpaca_output'])
    if index == -1:
        index = 0
    cleaned.append({    
        'sentiment': sentiment,
        'input' : d['input'],
        'reason' : d['alpaca_output'][index + len(sentiment):]
    })
    json.dump(cleaned, open('alpaca-gpt4-cleaned.json', 'w'), indent=4)