from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4')

class State(TypedDict):
    topic: str
    story: str
    translated_story: str

def llm_call_one(state: State):
    return {"story": [llm.invoke(f"Using the topic: {state['topic']}, write a 50 word story.")]}

def llm_call_two(state: State):
    return {"translated_story": [llm.invoke(f"Translate this {state['story']} to Japanese.")]}
    
graph = StateGraph(State)

graph.add_node(llm_call_one)
graph.add_node(llm_call_two)

graph.add_edge(START, "llm_call_one")
graph.add_edge("llm_call_one", "llm_call_two")
graph.add_edge("llm_call_two", END)

workflow = graph.compile()

