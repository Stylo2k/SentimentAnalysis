from classes import Classifier
from starlette.requests import Request

from ray import serve
from fastapi import FastAPI
from textblob import TextBlob

app = FastAPI()

import re

@serve.deployment
class TextBlobClassifier(Classifier):
    def __init__(self):
        self.model = TextBlob
    '''
    TextBlob takes as input one single sentence at a time
        - we classifiy the sentence by calling the TextBlob class
          with the given sentence
        - If the polarity is 0 then neutral, > 0 positive else negative
    '''
    def classify(self, text : str):
        polarity = self.model(text).sentiment.polarity
        
        
        
        if polarity > 0:
            response = "Positive"
        elif polarity == 0:
            response = "Neutral"
        else:
            response = "Negative"
        
        return response

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        return self.classify(text)


class TextBlobPreProcessor:
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
class TextBlobDeployment:
    def __init__(self, preprocessor, classifier):
        self.preprocessor = preprocessor
        self.classifier = classifier

    async def classify(self, text : str):
        preprocessed_text = self.preprocessor.preprocess(text)
        ref = await self.classifier.classify.remote(preprocessed_text)
        return await ref

    @app.post("/textblob")
    async def call(self, http_request: Request):
        text: str = await http_request.json()
        return self.classify(text)


text_blob = TextBlobDeployment.bind(TextBlobPreProcessor(), TextBlobClassifier.bind())