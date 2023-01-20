from classes import Classifier
from starlette.requests import Request

from ray import serve
from fastapi import FastAPI

import stanza

app = FastAPI()

import re
# TODO : run on bare metal
# TODO: possibly convert to a singleton that you get and then run the sentiment analysis on
@serve.deployment
class StanzaClassifier(Classifier):
    def __init__(self, model):
        self.model = model
    '''
    TextBlob takes as input one single sentence at a time
        - we classifiy the sentence by calling the TextBlob class
          with the given sentence
        - If the polarity is 0 then neutral, > 0 positive else negative
    '''
    def classify(self, text : str):
        doc = self.model(text)
        sentiment = 0
        size = len(doc.sentences)
        # Same concept as in the Issues notebook. We average out the sentiment over all sentences in a document.
        for i, sentence in enumerate(doc.sentences):
            sentiment += sentence.sentiment

        sentiment = sentiment / size

        polarity = round(sentiment, 0)
        
        response = {'text' : text, 'sentiment' : ''}
        
        if polarity == 0:
            response['sentiment'] = "Negative"
        elif polarity == 1:
            response['sentiment'] = "Neutral"
        else:
            response['sentiment'] = "Positive"
        
        return response

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        return self.classify(text)


class StanzaPreProcessor:
    def __init__(self):
        pass

    def preprocess(self, text : str):
        # remove any special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # remove any leading or trailing whitespaces
        text = text.strip()
        # remove any double whitespaces
        text = re.sub(r'\s+', ' ', text)
        # remove any html or markdown tags
        text = re.sub(r'<[^>]+>', '', text)
        # remove any urls
        text = re.sub(r'http\S+', '', text)
        # remove any emails
        text = re.sub(r'\S+@\S+', '', text)
        # remove any numbers
        # text = re.sub(r'\d+', '', text)
        return text

@serve.deployment
@serve.ingress(app)
class StanzaDeployment:
    def __init__(self, preprocessor, classifier):
        self.preprocessor = preprocessor
        self.classifier = classifier

    async def classify(self, text : str):
        preprocessed_text = self.preprocessor.preprocess(text)
        ref = await self.classifier.classify.remote(preprocessed_text)
        return await ref

    @app.post("/stanza")
    async def call(self, http_request: Request):
        text: str = await http_request.json()
        return self.classify(text)

# stanza.download('en')
model = stanza.Pipeline(lang='en', processors='tokenize,sentiment')
stanza = StanzaDeployment.bind(StanzaPreProcessor(), StanzaClassifier.bind(model))