from strands import Agent
from strands.models.ollama import OllamaModel 
from strands_tools import calculator, current_time

model_id = OllamaModel(
        model_id="llama3.2:latest",
        host="http://localhost:11434"
    )

agent = Agent(
        model=model_id,
        tools=[calculator, current_time]
    )

message = "I am born on 30th of February 1990. What is my age in days"

response = agent(message)
print(response)