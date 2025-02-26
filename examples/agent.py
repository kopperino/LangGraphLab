from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

load_dotenv()

llm = ChatOpenAI(model='gpt-4')

@tool
def check_space():
    """Checks who is currently in space."""
    try:
        response = requests.get("http://api.open-notify.org/astros.json")
        
        response.raise_for_status()  
        
        data = response.json()
        
        if "people" in data:
            return data["people"]
        else:
            return {"error": "Unexpected response format"}
    
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}

@tool
def get_iss():
    """
    Retrieves the current position and other details of the International Space Station (ISS) from the 'Where the ISS At' API.

    Makes a GET request to the API endpoint for satellite ID 25544 (the ISS) and returns the response in JSON format. 
    If an error occurs during the request, it returns a dictionary with an error message.

    Returns:
        dict: A dictionary containing the ISS data (latitude, longitude, etc.) if the request is successful.
              If an error occurs, a dictionary with an error message is returned.

    Exceptions:
        - HTTPError: Raised if the HTTP request returns an error status code (e.g., 404, 500).
        - RequestException: Catches other issues related to the request (e.g., network problems).
        - General Exception: Catches any other errors that may occur during execution.

    """
    try:
        response = requests.get(f"https://api.wheretheiss.at/v1/satellites/25544")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}



tools = [check_space, get_iss]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Cletus from the Simpsons. Respond to the user in a way that Cletus would."),
    ("human", "{messages}"),
    ("placeholder", "{agent_scratchpad}")])

agent = create_react_agent(model=llm, tools=tools, prompt=prompt)


