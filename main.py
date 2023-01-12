from filecmp import cmp
from ray import serve
from starlette.requests import Request

from enum import Enum
from fastapi import FastAPI
from typing import Dict, List
from pydantic import BaseModel

# import "textblob" from the file inside the textblob folder
import textblob_classifier.classifier as tb
import vader_classifier.classifier as vd
import stanza_classifier.classifier as sc

app = FastAPI()

class Classifiers(Enum):
    text_blob = 'text_blob'
    vader = 'vader'
    stanza = 'stanza'

class Sentiment(Enum):
    natural  = 'natural'
    positive = 'positive'
    negative = 'negative'


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

class MulRequest(BaseModel):
    classifiers : List[Classifiers]
    text : List[str]

    class Config:
        schema_example = {
            "example" : {
                "classifiers" : ["text_blob", "vader"],
                "text" : [
                    "The food was allright",
                    "The food was great"
                ]
            }
        }

class CmpRequest(BaseModel):
    classifiers : List[Classifiers]
    text : List[str]

@serve.deployment(route_prefix="/se")
@serve.ingress(app)
class SentimentAnalysis:
    classifiers : Dict = {}
    
    def __init__(self, classifiers : Dict):
        self.classifiers = classifiers
    
    async def classify_sentence(self, classifier, sentence):
        return await classifier.classify.remote(sentence)

    async def classify_text(self, classifiers , text : str):
        results = []
        if not isinstance(classifiers, List):
            classifiers = [classifiers]
        
        for sentence in text:
            result = {}
            for classifier in classifiers:
                ref = await self.classify_sentence(classifier, sentence)
                name = self.get_classifier_name(self.classifiers, classifier).value
                result[name] = await ref
            results.append(result)
        return results
    
    @app.post("/")
    async def classify_list_text(self, se_request: SeRequest):
        request = se_request.dict()
        classifier = request.get('classifier', None)
        text = request.get('text', None)
        classifier = self.classifiers.get(classifier, None)
        return await self.classify_text(classifier, text)

    @app.post("/multiple")
    async def multiple_list_text(self, mul_request : MulRequest):
        request = mul_request.dict()
        classifiers = request.get('classifiers', None)
        text = request.get('text', None)
        results = {}
        ref_classifiers = []
        for classifier in classifiers:
            ref_classifiers.append(self.classifiers.get(classifier, None))
        
        results = await self.classify_text(ref_classifiers, text)

        return results

    @app.post('/compare')
    async def compare_list_text(self, cmp_request : CmpRequest):
        request = cmp_request.dict()
        classifiers = request.get('classifiers', None)
        text = request.get('text', None)
        results = {}
        ref_classifiers = []
        for classifier in classifiers:
            ref_classifiers.append(self.classifiers.get(classifier, None))
        
        results = await self.classify_text(ref_classifiers, text)
        
        return results
    
    def get_classifier_name(self, d, val):
        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0]
        return None


sentiment_analysis = SentimentAnalysis.bind(
    {
        Classifiers.text_blob : tb.text_blob,
        Classifiers.vader : vd.vader,
        # Classifiers.stanza : sc.stanza
    })