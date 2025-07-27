from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    result: str
    operator: str

def adder(state: AgentState) -> AgentState:
    """Adds two numbers."""
    state["result"] = str(state["number1"] + state["number2"])
    return state

def subtractor(state: AgentState) -> AgentState:
    """Subtracts two numbers."""
    state["result"] = str(state["number1"] - state["number2"])
    return state

def multiplier(state: AgentState) -> AgentState:
    """Multiplies two numbers."""
    state["result"] = str(state["number1"] * state["number2"])
    return state

def divider(state: AgentState) -> AgentState:
    """Divides two numbers."""
    if state["number2"] == 0:
        state["result"] = "Cannot divide by zero"
    else:
        state["result"] = str(state["number1"] / state["number2"])
    return state

def decider(state: AgentState) -> str:
    """Decides which operation to perform based on the operator."""
    if state["operator"] == "+":
        return "addition"
    elif state["operator"] == "-":
        return "subtraction"
    elif state["operator"] == "*":
        return "multiplication"
    elif state["operator"] == "/":
        return "division"
    else:
        raise ValueError("Unknown operator")


graph = StateGraph(AgentState)

graph.add_node("adder_node", adder)
graph.add_node("subtractor_node", subtractor)
graph.add_node("multiplier_node", multiplier)
graph.add_node("divider_node", divider)
graph.add_node("decider_node", lambda state: state)

graph.add_edge(START, "decider_node")
graph.add_conditional_edges(
    "decider_node",
    decider, {
        "addition": "adder_node",
        "subtraction": "subtractor_node",
        "multiplication": "multiplier_node",
        "division": "divider_node"
    })

graph.add_edge("adder_node", END)
graph.add_edge("subtractor_node", END)
graph.add_edge("multiplier_node", END)
graph.add_edge("divider_node", END)

app = graph.compile()

from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png(), format='png'))

#app.invoke({"number1": 10, "number2": 5, "operator": "+"})
print(app.invoke({"number1": 10, "number2": 5, "operator": "+"})["result"])  # Output: 15
#app.invoke({"number1": 10, "number2": 5, "operator": "-"})
print(app.invoke({"number1": 10, "number2": 5, "operator": "-"})["result"])  # Output: 5
#app.invoke({"number1": 10, "number2": 5, "operator": "*"})
print(app.invoke({"number1": 10, "number2": 5, "operator": "*"})["result"])  # Output: 50
#app.invoke({"number1": 10, "number2": 5, "operator": "/"})
print(app.invoke({"number1": 10, "number2": 5, "operator": "/"})["result"])  # Output: 2.0
#app.invoke({"number1": 10, "number2": 0, "operator": "/"})  # This will handle division by zero
print(app.invoke({"number1": 10, "number2": 0, "operator": "/"})["result"])  # Output: Cannot divide by zero