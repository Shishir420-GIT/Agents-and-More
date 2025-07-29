from strands import Agent   
from strands_tools import calculator, current_time

agent = Agent(tools=[calculator, current_time])

message = "I am born on 30th of February 1990. What is my age in days"

response = agent(message)
print(response)