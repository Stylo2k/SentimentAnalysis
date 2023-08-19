from turtle import mode
from sklearn.metrics import cohen_kappa_score
import json
import multiprocessing

# Load data
data = json.load(open('dataset_labelled_v6.json'))

models = [
    'alshakoush',
    'gpt',
    'vader',
    'stanza',
    'text_blob',
    'alpaca_bitcoin',
    'alpaca_nobitcoin'
]

alpaca_bitcoin_sentiments = []
alpaca_nobitcoin_sentiments = []

alshakoush_sentiments = []
gpt_sentiments = []

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
        



# do every combination
def getResults(models):
    results_matrix = [

    ]
        
    for model1 in models:
        model1_results = []
        for model2 in models:
            if (model1 == model2):
                model1_results.append(float(1))
            else:
                model1_sentiments = []
                model2_sentiments = []
                for piece in data:
                    if (piece['type'] != 'commit'):
                        continue

                    sentiments = piece['sentiment_analysis']

                    

                    for sentiment in sentiments:
                        
                        model = sentiment['classifier']
                        if (model not in models):
                            continue

                        sentiment_here = sentiment['sentiment']

                        if (model == model1):
                            model1_sentiments.append(seToInt(sentiment_here))
                        elif (model == model2):
                            model2_sentiments.append(seToInt(sentiment_here))
                model1_results.append(cohen_kappa_score(model1_sentiments, model2_sentiments))
        results_matrix.append(model1_results)
    return results_matrix

def makeTable(models, results_matrix):
    # make a table in markdown
    print('| |', end='')
    for model in models:
        print(model + '|', end='')
    print()
    print('|', end='')
    for model in models:
        print('---|', end='')
    print('---|')
    for i in range(len(models)):
        print('|' + models[i] + '|', end='')
        for j in range(len(models)):
            print(str(round(results_matrix[i][j], 3)) + '|', end='')
        print()
    print('\n\n')

def makeHeatMap(models, results_matrix, algo_name):
    # make a heatmap
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    df_cm = pd.DataFrame(results_matrix, index = [i for i in models],
                    columns = [i for i in models])
    
    plt.figure(figsize = (10,7), dpi=600)
    # increase the font size
    sns.set(font_scale=1.5)

    import matplotlib.colors as mcolors

    # use sns heatmap using shades of black
    
    # Define your custom color palette
    colors = ["whitesmoke", "black"]
    cmap_name = "custom_cmap"
    cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)
    
    sns.heatmap(df_cm, cmap=cmap, annot=True, vmin=0, vmax=1)

    
    file_name = f'{algo_name}_{"_".join(models)}.png'
    plt.savefig(file_name, dpi=1200)
    
import numpy as np

def fleiss_kappa(data):
    num_subjects = len(data)
    num_categories = len(data[0])
    num_raters = np.sum(data[0])
    
    # Calculate observed agreement
    observed_agreement = np.sum(data * data, axis=1) - num_raters
    
    # Calculate expected agreement
    p = np.sum(data, axis=0) / (num_subjects * num_raters)
    p_bar = np.mean(p)
    expected_agreement = num_subjects * (p_bar**2)
    
    # Calculate agreement beyond chance
    agreement_beyond_chance = observed_agreement - expected_agreement
    
    # Calculate chance agreement
    max_possible_agreement = num_raters * (num_raters - 1)
    chance_agreement = np.sum(agreement_beyond_chance) / (num_subjects * max_possible_agreement)
    
    # Calculate Fleiss' kappa
    fleiss_kappa = chance_agreement / (1 - chance_agreement)
    
    return fleiss_kappa



def getFleissResults(models):
    results_matrix = [

    ]

    for model1 in models:
        model1_results = []
        for model2 in models:
            if (model1 == model2):
                model1_results.append(float(1))
            else:
                model1_sentiments = []
                model2_sentiments = []
                for piece in data:
                    if (piece['type'] != 'commit'):
                        continue

                    sentiments = piece['sentiment_analysis']

                    

                    for sentiment in sentiments:
                        
                        model = sentiment['classifier']
                        if (model not in models):
                            continue

                        sentiment_here = sentiment['sentiment']

                        if (model == model1):
                            model1_sentiments.append(seToInt(sentiment_here))
                        elif (model == model2):
                            model2_sentiments.append(seToInt(sentiment_here))
                model1_results.append(fleiss_kappa(np.array([model1_sentiments, model2_sentiments])))
        results_matrix.append(model1_results)
    return results_matrix



def doCohenFlow(models):
    results_matrix = getResults(models)
    # makeTable(models, results_matrix)
    makeHeatMap(models, results_matrix, 'cohen')

def doFleissFlow(models):
    results_matrix = getFleissResults(models)
    makeTable(models, results_matrix)
    makeHeatMap(models, results_matrix, 'fleiss')

combinations = [
    models,
    ['vader', 'stanza', 'text_blob'],
    ['alshakoush', 'gpt'],
    ['alshakoush', 'vader', 'stanza', 'text_blob'],
    ['gpt', 'vader', 'stanza', 'text_blob'],
    ['alshaokush', 'alpaca_bitcoin', 'alpaca_nobitcoin'],
]


def doCohen():
    # Create a multiprocessing pool
    pool = multiprocessing.Pool()
    # Apply the doCohenFlow function to each combination in parallel
    pool.map(doCohenFlow, combinations)
    # Close the pool
    pool.close()
    pool.join()

# doFleiss()
doCohen()

