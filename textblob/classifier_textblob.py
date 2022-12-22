from starlette.requests import Request

import ray
from ray import serve

from textblob import TextBlob

@serve.deployment
class Classifier:
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
        
        response = {'text' : text, 'sentiment' : ''}
        
        if polarity > 0:
            response['sentiment'] = "Positive"
        elif polarity == 0:
            response['sentiment'] = "Neutral"
        else:
            response['sentiment'] = "Negative"
        
        return response

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        return self.classify(text)


classifier = Classifier.bind()
        