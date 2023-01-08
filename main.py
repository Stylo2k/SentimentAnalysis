import re
import ray
from ray import serve
from starlette.requests import Request

from enum import Enum
from fastapi import FastAPI
from typing import Dict, List
from pydantic import BaseModel

# import "textblob" from the file inside the textblob folder
import textblob_classifier.classifier as tb

app = FastAPI()

class Classifiers(Enum):
    text_blob = 'text_blob'


class SeRequest(BaseModel):
    classifier: Classifiers
    text: List[str]

    class Config:
        schema_extra = {
            "example": {
                "classifier": "text_blob",
                "text": [
                    "The food was allright",
                    "The food was great",
                ]
            }
        }

@serve.deployment(route_prefix="/se")
@serve.ingress(app)
class SentimentAnalysis:
    classifiers : Dict = {}
    
    def __init__(self, textblob_classifier):
        self.classifiers['text_blob'] = textblob_classifier

    async def classify_text(self, classifier, text : str):
        results = []
        for sentence in text:
            ref = await classifier.classify.remote(sentence)
            results.append(await ref)
        return results
    
    @app.post("/")
    async def classify_list_text(self, se_request: SeRequest):
        request = se_request.dict()
        classifier = request.get('classifier', None).value
        text = request.get('text', None)
        classifier = self.classifiers.get(classifier, None)
        return await self.classify_text(classifier, text)


text_blob = tb.TextBlobDeployment.bind(tb.TextBlobPreProcessor(), tb.TextBlobClassifier.bind())

sentiment_analysis = SentimentAnalysis.bind(text_blob)