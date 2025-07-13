import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPEN_AI_KEY"))

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


def process(state: AgentState) -> AgentState:
    """Process the current state by invoking the LLM with the messages."""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")

