import json
bitcoin = json.load(open('alpaca_bitcoin.json', 'r'))
no_bitcoin = json.load(open('alpaca_nobitcoin.json', 'r'))
labeled = json.load(open('dataset_labelled_v5.json', 'r'))

index = 0

for se in bitcoin:
    no_bitcoin_se = no_bitcoin[index]
    labeled[index]['sentiment_analysis'].append(
        {
            "classifier" : "alpaca_bitcoin",
            "sentiment" : f"{se['alpaca_output']}",
            "reason" : "none"
        }
    )
    labeled[index]['sentiment_analysis'].append(
        {
            "classifier" : "alpaca_nobitcoin",
            "sentiment" : f"{no_bitcoin_se['alpaca_output']}",
            "reason" : "none"
        }
    )
    index += 1

json.dump(labeled, open('dataset_labelled_v6.json', 'w'), indent=4)