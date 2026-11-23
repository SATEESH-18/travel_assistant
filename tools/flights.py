
import requests

from langchain_core.tools import tool

from config import DUFFEL_API_KEY


@tool
def flight_search(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = ""
):
    """
    Search available flights using Duffel.
    """

    if not DUFFEL_API_KEY:
        return {"error": "Duffel API key is missing."}

    url = "https://api.duffel.com/air/offer_requests"

    headers = {
        "Authorization": f"Bearer {DUFFEL_API_KEY}",
        "Duffel-Version": "v2",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    slices = [
        {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date
        }
    ]

    if return_date:

        slices.append({
            "origin": destination,
            "destination": origin,
            "departure_date": return_date
        })

    payload = {
        "data": {
            "slices": slices,
            "passengers": [
                {"type": "adult"}
            ],
            "cabin_class": "economy"
        }
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
            "error": "Duffel flight search failed",
            "details": str(error)
        }


def flight_search_agent(state):

    origin = state.get("origin", "")
    destination = state.get("destination", "")

    start_date = state.get("start_date", "")
    end_date = state.get("end_date", "")

    if not origin or not destination:

        state["flight_results"] = (
            "Flight search skipped: origin or destination missing."
        )

        return state

    if not start_date:

        state["flight_results"] = (
            "Flight search skipped: exact departure date missing."
        )

        return state

    try:

        result = flight_search.invoke({
            "origin": origin,
            "destination": destination,
            "departure_date": start_date,
            "return_date": end_date
        })

        state["flight_results"] = str(result)

    except Exception as error:

        state["flight_results"] = str(error)

    return state
