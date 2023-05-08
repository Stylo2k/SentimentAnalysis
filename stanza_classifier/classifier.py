from classes import Classifier
from starlette.requests import Request

import dill
from ray import serve
from fastapi import FastAPI
import os
import re
import stanza as stz

app = FastAPI()

STANZA_NAME = "stanza_model.pkl"

def startup_event():
    '''
    The startup event is called when the deployment is created
    We check if the Stanza model is already downloaded and serialized
    If not we download the model and serialize it
    '''
    if os.path.exists(STANZA_NAME) == False:
        stz.download('en')
        # Load the Stanza model
        nlp = stz.Pipeline('en')

        # Serialize the Stanza model using dill
        with open(STANZA_NAME, 'wb') as f:
            dill.dump(nlp, f)


@serve.deployment
class StanzaClassifier(Classifier):
    def __init__(self):
        # run the startup event
        startup_event()
        # if the file does not exist throw an error
        if os.path.exists(STANZA_NAME) == False:
            raise Exception("Stanza model not found")

        file = open(STANZA_NAME, 'rb')
        nlp = dill.load(file)
        self.model = nlp

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

        if (size == 0):
            return "Neutral"

        sentiment = sentiment / size

        polarity = round(sentiment, 0)
        
        response = {}
        
        if polarity == 0:
            response = "Negative"
        elif polarity == 1:
            response = "Neutral"
        else:
            response = "Positive"

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

stanza = StanzaDeployment.bind(
    StanzaPreProcessor(), 
    StanzaClassifier.bind()
)