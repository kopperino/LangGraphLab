from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class Route(BaseModel):
    step: Literal["Billing", "Fraud & Security", "Complaint Resolution"] = Field(
        description="The next step in the routing process."
    )

llm = ChatOpenAI(model='gpt-4')


class State(TypedDict):
    customer_query: str
    decision: str
    assistance: str


def router(state: State):
    router = llm.with_structured_output(Route)
    decision = router.invoke(f"""Using the customer query: {state['customer_query']}, 
                                    route the customer to the appropriate agent""")
    return {"decision": decision.step}

def billing_agent(state: State):
    return {"assistance": llm.invoke(f"""You are a professional billing agent. 
                                     Help the customer based on the query: {state['customer_query']}""")}

def fraud_and_security_agent(state: State):
    return {"assistance": llm.invoke(f"""You are a professional fraud and security agent. 
                                     Help the customer based on the query: {state['customer_query']}""")}

def complaint_resolution_agent(state: State):
    return {"assistance": llm.invoke(f"""You are a professional complaint resolution agent. 
                                     Help the customer based on the query: {state['customer_query']}""")}

def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "Billing":
        return "billing_agent"
    elif state["decision"] == "Fraud & Security":
        return "fraud_and_security_agent"
    elif state["decision"] == "Complaint Resolution":
        return "complaint_resolution_agent"

graph = StateGraph(State)

graph.add_node(router)
graph.add_node(billing_agent)
graph.add_node(fraud_and_security_agent)
graph.add_node(complaint_resolution_agent)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "billing_agent": "billing_agent",
        "fraud_and_security_agent": "fraud_and_security_agent",
        "complaint_resolution_agent": "complaint_resolution_agent",
    },
)

graph.add_edge("billing_agent", END)
graph.add_edge("fraud_and_security_agent", END)
graph.add_edge("complaint_resolution_agent", END)

compiled_graph = graph.compile()


