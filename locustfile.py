from locust import task, between, HttpUser

DATA =  {
 'text' : [
    "The food was allright",
    "The food was great",
    "The food was terrible",
    "The food was amazing",
    "that was the best food I've ever had",
    "I would never eat there again",
    "I would eat there every day if I could",
    "I would pay $100 for a meal there",
],
    'classifier' : 'text_blob'
}

class TextBlob(HttpUser):
    wait_time = between(1, 5)

    @task
    def main(self):
        self.client.post("/", json=DATA)
