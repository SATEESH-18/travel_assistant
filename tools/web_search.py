
import requests

from langchain_core.tools import tool

from config import TAVILY_API_KEY


@tool
def web_search(query: str):
    """
    Search travel information using Tavily.
    """

    if not TAVILY_API_KEY:
        return {"error": "Tavily API key is missing."}

    url = "https://api.tavily.com/search"

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "search_depth": "advanced",
        "max_results": 8
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        return {
            "error": "Tavily search failed",
            "details": str(error)
        }


def web_search_agent(state):

    query = f"""
Travel research for the following trip:

Origin: {state.get("origin", "")}

Destination: {state.get("destination", "")}

Dates: {state.get("dates_description", "")}

Budget: {state.get("budget", "")}

Preferences: {state.get("preferences", "")}

Find:

- Tourist attractions
- Food experiences
- Cultural experiences
- Technology attractions
- Transportation
- Neighborhoods
- Approximate costs
- Practical travel tips
- Current travel information
"""

    try:

        result = web_search.invoke({
            "query": query
        })

        state["research_results"] = str(result)

    except Exception as error:

        state["research_results"] = str(error)

    return state
