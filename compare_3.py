import json
import krippendorff

# Load data
data = json.load(open('dataset_labelled.json'))

models = [
    'vader',
    'stanza',
    'text_blob'
]


vader_sentiments = []
stanza_sentiments = []
text_blob_sentiments = []


def seToInt(se):
    se = se.lower()
    if (se == 'positive'):
        return 1
    elif (se == 'negative'):
        return -1
    else:
        return 0

for piece in data:
    if (piece['type'] != 'commit'):
        continue

    sentiments = piece['sentiment']

    for model in models:
        if (model not in sentiments):
            continue

        sentiment = sentiments[model]

        if (model == 'vader'):
            vader_sentiments.append(seToInt(sentiment))
        elif (model == 'stanza'):
            stanza_sentiments.append(seToInt(sentiment))
        elif (model == 'text_blob'):
            text_blob_sentiments.append(seToInt(sentiment))
        else:
            continue
        

All = [vader_sentiments, stanza_sentiments, text_blob_sentiments]

print('All: ' + str(krippendorff.alpha(reliability_data=All)))



