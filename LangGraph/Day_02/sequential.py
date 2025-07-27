from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):               
    name : str
    age : int
    result : str
    
def first_node(state: AgentState) -> AgentState:
    """First node to process the name and greet the user."""
    state["result"] = f"Hello {state['name']},"
    return state

def second_node(state: AgentState) -> AgentState:
    """Second node to process the age and complete the greeting."""
    state["result"] += f" you are {state['age']} years old."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")

app = graph.compile()

from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png(), format='png'))

result = app.invoke({"name": "Bob", "age": 25})
print(result["result"])  # Output: Hello Bob, you are 25 years old.