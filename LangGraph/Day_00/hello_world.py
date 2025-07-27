from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class ChatState(TypedDict):
    response: str

def welcome_node(state: ChatState) -> ChatState:
    """
    Returns a personalized welcome message.
    """
    state['response'] = f"👋 Welcome! {state['response']} Enjoy exploring LangGraph."
    return state

graph = StateGraph(ChatState)

graph.add_node("welcome", welcome_node)
graph.set_entry_point("welcome")
graph.set_finish_point("welcome")

app = graph.compile()

from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png(), format='png'))

result = app.invoke({"response": "Glad to see you here."})
print(result['response'])