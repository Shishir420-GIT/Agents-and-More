import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from dotenv import load_dotenv
load_dotenv()

class ConversationState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def sum_numbers(x: int, y: int) -> int:
    """Returns the sum of two integers."""
    return x + y

@tool
def difference(x: int, y: int) -> int:
    """Returns the difference between two integers."""
    return x - y

@tool
def product(x: int, y: int) -> int:
    """Returns the product of two integers."""
    return x * y

toolset = [sum_numbers, difference, product]

llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPEN_AI_KEY")).bind_tools(toolset)

def agent_step(state: ConversationState) -> ConversationState:
    """Run the LLM with the current conversation."""
    sys_msg = SystemMessage(
        content="You are an intelligent assistant. Help users as best as you can."
    )
    reply = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [reply]}

def continue_decision(state: ConversationState):
    """Check if further action is needed."""
    msgs = state["messages"]
    last = msgs[-1]
    if not last.tool_calls:
        return "finish"
    else:
        return "proceed"

workflow = StateGraph(ConversationState)
workflow.add_node("assistant_node", agent_step)

tool_handler = ToolNode(tools=toolset)
workflow.add_node("tool_handler", tool_handler)

workflow.set_entry_point("assistant_node")

workflow.add_conditional_edges(
    "assistant_node",
    continue_decision, {
        "proceed": "tool_handler",
        "finish": END
    }
)

workflow.add_edge("tool_handler", "assistant_node")

pipeline = workflow.compile()

def display_stream(stream):
    for item in stream:
        msg = item["messages"][-1]
        if isinstance(msg, tuple):
            print(msg)
        else:
            msg.pretty_print()

user_input = {
    "messages": [("user", "What is 15 plus 27, then subtract 10 from the result? And can you share a fun fact?")]
}
display_stream(pipeline.stream(user_input, stream_mode="values"))
