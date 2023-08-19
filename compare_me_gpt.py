import json
import krippendorff

# Load data
data = json.load(open('dataset_labelled_v4.json'))

models = [
    'alshakoush',
    'gpt',
    'vader',
    'stanza',
    'text_blob',
    'alpaca_bitcoin',
    'alpaca_nobitcoin'
]

alshakoush_sentiments = []
gpt_sentiments = []

alpaca_bitcoin_sentiments = []
alpaca_nobitcoin_sentiments = []

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

    sentiments = piece['sentiment_analysis']

    

    for sentiment in sentiments:
        
        model = sentiment['classifier']
        if (model not in models):
            continue

        sentiment_here = sentiment['sentiment']

        if (model == 'alshakoush'):
            alshakoush_sentiments.append(seToInt(sentiment_here))
        elif (model == 'gpt'):
            gpt_sentiments.append(seToInt(sentiment_here))
        elif (model == 'vader'):
            vader_sentiments.append(seToInt(sentiment_here))
        elif (model == 'stanza'):
            stanza_sentiments.append(seToInt(sentiment_here))
        elif (model == 'text_blob'):
            text_blob_sentiments.append(seToInt(sentiment_here))
        elif (model == 'alpaca_bitcoin'):
            alpaca_bitcoin_sentiments.append(seToInt(sentiment_here))
        elif (model == 'alpaca_nobitcoin'):
            alpaca_nobitcoin_sentiments.append(seToInt(sentiment_here))
        

me_and_gpt =  [alshakoush_sentiments, gpt_sentiments]
print('Me & GPT: ' + str(krippendorff.alpha(reliability_data=me_and_gpt)))

me_and_alpaca_bitcoin = [alshakoush_sentiments, alpaca_bitcoin_sentiments]
print('Me & Alpaca Bitcoin: ' + str(krippendorff.alpha(reliability_data=me_and_alpaca_bitcoin)))

me_and_alpaca_nobitcoin = [alshakoush_sentiments, alpaca_nobitcoin_sentiments]
print('Me & Alpaca No Bitcoin: ' + str(krippendorff.alpha(reliability_data=me_and_alpaca_nobitcoin)))

alpaca_bitcoin_and_alpaca_nobitcoin = [alpaca_bitcoin_sentiments, alpaca_nobitcoin_sentiments]
print('Alpaca Bitcoin & Alpaca No Bitcoin: ' + str(krippendorff.alpha(reliability_data=alpaca_bitcoin_and_alpaca_nobitcoin)))


me_and_other = [alshakoush_sentiments, vader_sentiments, stanza_sentiments, text_blob_sentiments]
print('Me & Other: ' + str(krippendorff.alpha(reliability_data=me_and_other)))

gpt_and_other = [gpt_sentiments, vader_sentiments, stanza_sentiments, text_blob_sentiments]
print('GPT & Other: ' + str(krippendorff.alpha(reliability_data=gpt_and_other)))



