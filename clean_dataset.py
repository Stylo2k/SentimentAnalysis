import json
import requests


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data



# data = read_json_file('datasets/Commit Mining/terraform_tf_keywords.json')
data = read_json_file(f'dataset_labelled_v2.json')

all_text = []

new_data = []
        
for element in data:
    sentiment = element.get('sentiment')
    if not sentiment:
        continue
    
    text_blob = sentiment.get('text_blob').lower()
    vader = sentiment.get('vader').lower()
    stanza = sentiment.get('stanza').lower()


    gpt = sentiment.get('gpt')

    reason_none = 'none'
    # gpt is a json string make it a dict
    # load the json string as JSON, allow for non enclosed double quotes
    
    
    # replace the word reason with "reason"
    
    gpt = gpt.replace('reason:', '"reason":')
    gpt = gpt.replace('Reason:', '"reason":')
    gpt = gpt.replace('"Reason":', '"reason":')
    gpt = gpt.replace('"Sentiment":', '"sentiment":')
    gpt = json.loads(gpt)
    
    gpt['sentiment'] = gpt.get('sentiment').lower()

    data_dict = [
        {
            'classifier' : 'text_blob',
            'sentiment' : text_blob,
            'reason' : reason_none
        },
        {
            'classifier' : 'vader',
            'sentiment' : vader,
            'reason' : reason_none
        },
        {
            'classifier' : 'stanza',
            'sentiment' : stanza,
            'reason' : reason_none
        },
        {
            'classifier' : 'gpt',
            'sentiment' : gpt.get('sentiment'),
            'reason' : gpt.get('reason')
        }
    ]
    del element['sentiment']
    element['sentiment_analysis'] = data_dict
    new_data.append(element)

issues = []
    
for element in data:
    sentiment = element.get('sentiment_analysis')
    if not sentiment:
        issues.append(element)
        # new_data.append(element)
    
with open('dataset_issues.json', 'w') as f:
    json.dump(issues, f, indent=4)
    
