from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    result: str
    name: str

def process_values(state: AgentState) -> AgentState:
    "This function processes the input values and returns a result."
    state['result'] = f"Hi!! {state['name']} your sum is {str(sum(state['values']))}"
    return state

graph = StateGraph[AgentState]

graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")


app = graph.compile()

from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png(), format='png'))

result = app.invoke({
    "values": [1, 2, 3, 4, 5,6],
    "name": "Shishir",
})

print(result['result'])  # Output: Hi!! Shishir your sum is 15