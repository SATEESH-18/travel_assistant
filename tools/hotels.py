
import requests

from langchain_core.tools import tool

from config import LITEAPI_API_KEY


@tool
def hotel_search(
    location: str,
    check_in: str,
    check_out: str,
    adults: int = 1
):
    """
    Search hotel rates using LiteAPI.
    """

    if not LITEAPI_API_KEY:
        return {"error": "LiteAPI key is missing."}

    url = "https://api.liteapi.travel/v3.0/hotels/rates"

    headers = {
        "X-API-Key": LITEAPI_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "occupancies": [
            {"adults": adults}
        ],
        "currency": "USD",
        "guestNationality": "IN",
        "checkin": check_in,
        "checkout": check_out,
        "aiSearch": f"hotels in {location}",
        "roomMapping": True,
        "maxRatesPerHotel": 1,
        "includeHotelData": True
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
            "error": "LiteAPI hotel search failed",
            "details": str(error)
        }


def hotel_search_agent(state):

    destination = state.get("destination", "")
    start_date = state.get("start_date", "")
    end_date = state.get("end_date", "")

    if not destination:

        state["hotel_results"] = (
            "Hotel search skipped: destination missing."
        )

        return state

    if not start_date or not end_date:

        state["hotel_results"] = (
            "Hotel search skipped: exact check-in "
            "and check-out dates missing."
        )

        return state

    try:

        result = hotel_search.invoke({
            "location": destination,
            "check_in": start_date,
            "check_out": end_date,
            "adults": 1
        })

        state["hotel_results"] = str(result)

    except Exception as error:

        state["hotel_results"] = str(error)

    return state
