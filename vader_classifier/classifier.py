from classes import Classifier
from starlette.requests import Request

from ray import serve
from fastapi import FastAPI

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

import re

@serve.deployment
class VaderClassifier(Classifier):
    def __init__(self):
        self.model = SentimentIntensityAnalyzer()
    '''
    Vader takes as input one single sentence at a time
        - we classifiy the sentence by calling the Vader class
          with the given sentence
    '''
    def classify(self, text : str):
        polarity = self.model.polarity_scores(text)
        
        
        if polarity['compound'] >= 0.05 :
            response = "Positive"
        elif polarity['compound'] <= - 0.05 :
            response = "Negative"
        else :
            response = "Neutral"
        
        return response

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        return self.classify(text)


class VaderPreProcessor:
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
        return text

@serve.deployment
@serve.ingress(app)
class VaderDeployment:
    def __init__(self, preprocessor, classifier):
        self.preprocessor = preprocessor
        self.classifier = classifier

    async def classify(self, text : str):
        preprocessed_text = self.preprocessor.preprocess(text)
        ref = await self.classifier.classify.remote(preprocessed_text)
        return await ref

    @app.post("/vader")
    async def call(self, http_request: Request):
        text: str = await http_request.json()
        return self.classify(text)


vader = VaderDeployment.bind(VaderPreProcessor(), VaderClassifier.bind())