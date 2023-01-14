from enum import Enum
from pydantic import BaseModel
from typing import List



class Classifier:
    def classify(self, text):
        raise NotImplementedError

class Classifiers(Enum):
    text_blob = 'text_blob'
    vader = 'vader'
    stanza = 'stanza'

class Sentiment(Enum):
   @classmethod
   def _missing_(cls, value):
      for member in cls:
         if member.value == value.lower():
            return member
   natural = 'neutral'
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

class LabeledText(BaseModel):
    sentence : str
    sentiment : Sentiment

    class Config:
        schema_example = {
            "example" : {
                "sentence" : "The food was all right",
                "sentiment" : "neutral"
            }
        }

class CmpRequest(BaseModel):
    classifiers : List[Classifiers]
    text : List[LabeledText]

    class Config:
        schema_example = {
            "example" : {
                "classifiers" : ["text_blob", "vader"],
                "text" : [
                    {
                        "sentence" : "The food was all right",
                        "sentiment" : "neutral"
                    }
                ]
            }
        }