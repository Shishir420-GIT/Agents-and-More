from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import random

class AgentState(TypedDict):
    name: str
    counter: int
    counts: List[int]
    result: str

def greeting_node(state: AgentState) -> AgentState:
    """Initial node to greet the user and set up the state."""
    state["result"] = f"Hello {state['name']}!"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """ Node that generates a random number and updates the state."""
    state["counter"] += 1
    state["counts"].append(random.randint(1, 100))
    return state

def should_continue(state: AgentState) -> str:
    """Condition to check if the loop should continue."""
    if state["counter"] < 5:
        return "loop"
    else:
        state["result"] += f", your counts are {state['counts']}" # bug needs to be fixed
        return "exit"
    
graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    should_continue, {
        "loop": "random",
        "exit": END
    }
)
graph.set_entry_point("greeting")

app = graph.compile()

from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png(), format='png'))

result = app.invoke({
    "name": "Shishir",
    "counter": 0,
    "counts": [],
    "result": ""
})

print("Final Result: ", result["result"])