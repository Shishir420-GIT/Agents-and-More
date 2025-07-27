import os
from dotenv import loadenv
import openai

loadenv()

# Load your API key securely (e.g., from an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a chat completion
response = openai.ChatCompletion.create(
    model="gpt-4",  # Replace with the correct model name
    messages=[
        {"role": "user", "content": "write a haiku about AI"}
    ]
)



strr = "shishir"

newLIST = strr.split()
print(newLIST)
# Print the generated haiku
print(response['choices'][0]['message']['content'])
