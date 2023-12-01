from itertools import combinations
from turtle import mode
from sklearn.metrics import cohen_kappa_score
import json
import multiprocessing
import krippendorff
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
data = json.load(open('dataset_labelled_v7.json'))

models = [
    'alshakoush',
    'gpt',
    'vader',
    'stanza',
    'text_blob',
    'alpaca_bitcoin',
    'alpaca_nobitcoin',
    'alpaca_gpt4'
]

alpaca_gpt4_sentiments = []
alpaca_bitcoin_sentiments = []
alpaca_nobitcoin_sentiments = []
vanilla_alpaca_sentiments = []

alshakoush_sentiments = []
gpt_sentiments = []

vader_sentiments = []
stanza_sentiments = []
text_blob_sentiments = []

LISTS_MAPPING = {
    'alshakoush': alshakoush_sentiments,
    'gpt': gpt_sentiments,
    'vader': vader_sentiments,
    'stanza': stanza_sentiments,
    'text_blob': text_blob_sentiments,
    'alpaca_bitcoin': alpaca_bitcoin_sentiments,
    'alpaca_nobitcoin': alpaca_nobitcoin_sentiments,
    'alpaca_gpt4': alpaca_gpt4_sentiments,
}


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
        
        LISTS_MAPPING[model].append(seToInt(sentiment_here))
        

ALGO_MAPPING = {
    'cohen': cohen_kappa_score,
    'krippendorff': lambda modelX, modelY : krippendorff.alpha(reliability_data=[modelX, modelY])
}

# do every combination
def getResults(models, algo):
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
                model1_results.append(ALGO_MAPPING[algo](model1_sentiments, model2_sentiments))
        results_matrix.append(model1_results)
    return results_matrix


def makeHeatMap(models, results_matrix, algo_name):
    # make a heatmap

    df_cm = pd.DataFrame(results_matrix, index = [i for i in models],
                    columns = [i for i in models])
    
    
    plt.figure(figsize = (15,15), dpi=300)
    # increase the font size
    sns.set(font_scale=1.5)

    import matplotlib.colors as mcolors

    # use sns heatmap using shades of black
    
    # Define your custom color palette
    colors = ["whitesmoke", "black"]
    cmap_name = "custom_cmap"
    cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)
    
    sns.heatmap(df_cm, cmap=cmap, annot=True, vmin=0, vmax=1, fmt='.2f')

    
    file_name = f'images/all/{algo_name}_{"_".join(models)}.png'
    plt.savefig(file_name, dpi=150)
    

figure_names = {
    'alshakoush' : 'alshakoush',
    'gpt' : 'gpt',
    'vader': 'vader',
    'stanza': 'stanza',
    'text_blob': 'text_blob',
    'alpaca_bitcoin': 'alpacaB',
    'alpaca_nobitcoin': 'alpacaNB',
    'alpaca_gpt4': 'alpacaGPT4',
}


def doCohenFlow(models):
    results_matrix = getResults(models, 'cohen')    
    models = [
        figure_names[model] for model in models 
    ]
    print(models)
    
            
    makeHeatMap(models, results_matrix, 'cohen')

def doKrippendorffFlow(models):
    results_matrix = getResults(models, 'krippendorff')    
    models = [
        figure_names[model] for model in models 
    ]
    print(models)
    
            
    makeHeatMap(models, results_matrix, 'krippendorff')

import itertools
# now take every combination possible from the models start with 2 and go up to len(models)
wanted_combinations = [models]
# for length in range(2, len(models) + 1):
#     local_combi = list(itertools.combinations(models, length))
#     combinations.extend(local_combi)
    


def doCohen():
    # Create a multiprocessing pool
    pool = multiprocessing.Pool()
    # Apply the doCohenFlow function to each combination in parallel
    pool.map(doCohenFlow, wanted_combinations)
    # Close the pool
    pool.close()
    pool.join()


def doKrippendorff():
    # Create a multiprocessing pool
    pool = multiprocessing.Pool()
    # Apply the doCohenFlow function to each combination in parallel
    pool.map(doKrippendorffFlow, wanted_combinations)
    # Close the pool
    pool.close()
    pool.join()


# doCohen()
doKrippendorff()