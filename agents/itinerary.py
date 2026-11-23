
from langchain_groq import ChatGroq

from config import GROQ_API_KEY


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)


def itinerary_agent(state):

    prompt = f"""
You are a professional travel itinerary planner.

Create a practical day-by-day travel itinerary.

USER REQUIREMENTS
=================

Origin: {state.get("origin", "")}

Destination: {state.get("destination", "")}

Dates: {state.get("dates_description", "")}

Start date: {state.get("start_date", "")}

End date: {state.get("end_date", "")}

Budget: {state.get("budget", "")}

Preferences: {state.get("preferences", "")}


FLIGHTS
=======

{state.get("flight_results", "No flight information available.")}


HOTELS
======

{state.get("hotel_results", "No hotel information available.")}


WEB RESEARCH
============

{state.get("research_results", "No web research available.")}


WEATHER
=======

{state.get("weather_results", "No weather information available.")}


IMPORTANT RULES
===============

1. Never invent flight prices.
2. Never invent hotel prices.
3. Never invent availability.
4. Clearly mention missing travel dates.
5. Distinguish current weather from future forecasts.
6. Respect the user's budget.
7. Include food, technology and cultural experiences.
8. Include transportation suggestions.
9. Create a practical day-by-day itinerary.
10. Identify assumptions and missing information.
11. Do not claim that a booking has been made.
12. Do not invent facts that are absent from research.

Create a detailed itinerary with:

- Trip overview
- Day-by-day schedule
- Food recommendations
- Technology experiences
- Cultural experiences
- Transportation
- Budget considerations
- Travel tips
"""

    try:

        response = llm.invoke(prompt)

        state["itinerary"] = response.content

    except Exception as error:

        state["itinerary"] = (
            f"Itinerary generation failed: {str(error)}"
        )

    return state


def final_llm_agent(state):

    prompt = f"""
You are the final AI travel assistant.

Answer the user's original question.

USER QUESTION
=============

{state.get("user_question", "")}


GENERATED ITINERARY
===================

{state.get("itinerary", "")}


RULES
=====

- Be clear and useful.
- Do not invent information.
- Respect the user's budget.
- Mention missing dates.
- Explain skipped flight and hotel searches.
- Never present current weather as a future forecast.
- Use headings and bullet points.
- Clearly distinguish estimated costs from live prices.
- Never claim that a reservation was completed.

Return the final travel recommendation.
"""

    try:

        response = llm.invoke(prompt)

        state["final_response"] = response.content

    except Exception as error:

        state["final_response"] = (
            f"Final response generation failed: {str(error)}"
        )

    return state
