import os
import openai
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

text = "Removed the default use of detailed monitoring. (#17)\n\n* Reduces CloudWatch costs for metrics by 80%"

response = openai.Completion.create(
  model="text-davinci-003",
  prompt= f"Use JSON to format the response like this:\n\n{{sentiment: \"sentiment here\", reason: \"reason here\"}}. Classify the sentiment of the following sentence and given me the reason:\n\n{text}\n",
  temperature=0,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print(response)
