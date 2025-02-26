from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated, Literal
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model='gpt-4')

class State(TypedDict):
    topic: str
    poem: str
    feedback: str
    good_or_bad: str

class Feedback(BaseModel):
    grade: Literal["good", "bad"] = Field(
        description="Decide if the poem is good or bad"
    )
    feedback: str = Field(description="If the poem is bad, give feedback to improve it")

evaluator = llm.with_structured_output(Feedback)

def llm_generator(state: State):
    if state.get('feedback'):
        msg = llm.invoke(f"Write a 50 word poem about {state['topic']} but also account for the feedback: {state['feedback']}")
    else:
        msg = llm.invoke(f"Write a 50 word poem about {state['topic']}")
    return {"poem": msg.content}

def llm_evaluator(state: State):
    grade = evaluator.invoke(f"Grade the poem as good or bad {state['poem']}, if it does not have the word Sinan in it, grade it bad immediately")

    return {"good_or_bad": grade.grade, "feedback": grade.feedback}

def route(state: State):
    if state['good_or_bad'] == "good":
        return "Accepted"
    else:
        return "Denied"
    
graph = StateGraph(State)

graph.add_node(llm_evaluator)
graph.add_node(llm_generator)

graph.add_edge(START, "llm_generator")
graph.add_edge("llm_generator", "llm_evaluator")
graph.add_conditional_edges(
    "llm_evaluator",
    route,
    {
        "Accepted": END,
        "Denied": "llm_generator"
    }
)

compiled_graph = graph.compile()