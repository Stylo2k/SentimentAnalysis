from starlette.requests import Request

import ray
from ray import serve

from transformers import pipeline


@serve.deployment
class Classify:
    def __init__(self):
        self.model = pipeline("text-classification")

    def classify(self, text: str) -> str:
        model_output = self.model(text)
        sentiment = model_output[0].get('label').capitalize()
        
        response = {}

        return response

    async def __call__(self, http_request: Request) -> str:
        text: str = await http_request.json()
        return self.classify(text)


classifier = Classify.bind()