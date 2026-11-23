
import requests

from langchain_core.tools import tool

from config import OPENWEATHER_API_KEY


@tool
def weather_search(location: str):
    """
    Get current weather using OpenWeather.
    """

    if not OPENWEATHER_API_KEY:
        return {"error": "OpenWeather API key is missing."}

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        return {
            "error": "Weather search failed",
            "details": str(error)
        }


def weather_search_agent(state):

    destination = state.get("destination", "")

    if not destination:

        state["weather_results"] = (
            "Weather search skipped: destination missing."
        )

        return state

    try:

        result = weather_search.invoke({
            "location": destination
        })

        state["weather_results"] = str(result)

    except Exception as error:

        state["weather_results"] = str(error)

    return state
