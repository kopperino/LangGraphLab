from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4')

class State(TypedDict):
    topic: str
    character_count: int

    world_building: str
    conflicts: str
    characters: str
    random_event: str

    final_story: str


def generate_world_building(state: State):
    return {"world_building": llm.invoke(f"""You are a master world-builder specialising in creating immersive and captivating story settings. 
                                         Using the topic: '{state['topic']}', 
                                         craft a richly detailed world that serves as the foundation for a compelling narrative. 
                                         Consider key aspects such as geography, culture, history, 
                                         societal structure, technology or magic (if applicable), 
                                         and any unique elements that make this world distinct. 
                                         Ensure the world feels alive, with conflicts, mysteries, and opportunities for adventure.
                                         """)}

def generate_conflicts(state: State):
    return {"conflicts": llm.invoke(f"""
                                    You are an expert storyteller with a deep understanding of narrative tension and character development. 
                                    Based on the topic '{state['topic']}', identify compelling conflicts that will drive the story forward. 
                                    Consider:
                                    Internal struggles: the protagonists fears, doubts, or moral dilemmas.
                                    External threats: antagonists, societal pressures, or environmental challenges.
                                    Unexpected challenges: surprising twists or obstacles that disrupt the protagonists journey.
                                    Ensure the conflicts create tension, growth, and high stakes that keep the audience engaged.
                                    """)}

def generate_characters(state: State):
    return {"characters": llm.invoke(f"""You are an expert character developer with a talent for crafting compelling and multidimensional characters. 
                                     Based on the topic '{state['topic']}', create {state['character_count']} unique characters. 
                                     Describe their names, backgrounds, and personalities, including their strengths, flaws, and motivations. 
                                     Explain their roles in the story, how they interact with other characters, and the key challenges or conflicts they face. 
                                     Ensure each character is distinct, deeply developed, and contributes meaningfully to the story’s progression.
                                     """)}

def generate_random_event(state: State):
    return {"random_event": llm.invoke("""Introduce a surprising and impactful event that adds depth and excitement to the story. 
                                       The event should be unexpected yet fit naturally within the narrative, 
                                       creating tension, driving character development, or shifting the story’s direction. 
                                       It could be a sudden twist, an unforeseen obstacle, an unusual discovery, 
                                       or a dramatic turning point that challenges the characters in meaningful ways.
                                       """)}


def aggregate(state: State):
    return {"final_story": llm.invoke(f"""You are an expert storyteller with a mastery of narrative structure, character development, and immersive world-building. 
                                      Using the following elements—characters: {state['characters']}, 
                                      conflicts: {state['conflicts']}, random event: {state['random_event']}, and world-building: {state['world_building']}—
                                      craft a captivating and cohesive story. 
                                      Ensure the narrative flows naturally, with well-paced tension, meaningful character arcs, and vivid descriptions that bring the world to life. 
                                      The story should be engaging, immersive, and emotionally compelling, leaving a lasting impact on the reader.
                                      """)}

graph = StateGraph(State)

graph.add_node(generate_world_building)
graph.add_node(generate_conflicts)
graph.add_node(generate_characters)
graph.add_node(generate_random_event)
graph.add_node(aggregate)

graph.add_edge(START, "generate_world_building")
graph.add_edge(START, "generate_conflicts")
graph.add_edge(START, "generate_characters")
graph.add_edge(START, "generate_random_event")

graph.add_edge("generate_world_building", "aggregate")
graph.add_edge("generate_conflicts", "aggregate")
graph.add_edge("generate_characters", "aggregate")
graph.add_edge("generate_random_event", "aggregate")

graph.add_edge("aggregate", END)

compiled_graph = graph.compile()