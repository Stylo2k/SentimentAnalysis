'''
    Locust file for testing the deployment of the Sentiment Analysis API under load.
'''
from locust import task, between, HttpUser

classifiers = ['text_blob', 'vader']

text = [
    "The food was allright",
    "The food was great",
    "The food was terrible",
    "The food was amazing",
    "that was the best food I've ever had",
    "I would never eat there again",
    "I would eat there every day if I could",
    "I would pay $100 for a meal there",
]

labelled_text = [
    {
        "sentence" : "The food was all right",
        "sentiment" : "neutral"
    },
    {
        "sentence" : "The food was great",
        "sentiment" : "positive"
    },
    {
        "sentence" : "The food was terrible",
        "sentiment" : "negative"
    },
    {
        "sentence" : "The food was amazing",
        "sentiment" : "positive"
    },
    {
        "sentence" : "that was the best food I've ever had",
        "sentiment" : "positive"
    },
    {
        "sentence" : "I would never eat there again",
        "sentiment" : "negative"
    }
]

ONE_CLASSIFIER =  {
    'text' : text,
    'classifier' : 'text_blob'
}

MULTIPLE_CLASSIFIERS =  {
    'text' : text,
    'classifiers' : classifiers
}

COMPARE_CLASSIFIERS =  {
    'text' : labelled_text,
    'classifiers' : classifiers
}


class SentimentAnalysis(HttpUser):
    wait_time = between(1, 5)

    @task
    def main(self):
        self.client.post("/", json=ONE_CLASSIFIER)
    @task
    def multiple(self):
        self.client.post("/multiple", json=MULTIPLE_CLASSIFIERS)
    @task
    def compare(self):
        self.client.post("/compare", json=COMPARE_CLASSIFIERS)


