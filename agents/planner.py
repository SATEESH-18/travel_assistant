
import json
import re

from datetime import date
from typing import TypedDict

from pydantic import BaseModel, Field, field_validator

from langchain_groq import ChatGroq

from config import GROQ_API_KEY


# =====================================================
# LANGGRAPH STATE
# =====================================================

class AgentState(TypedDict, total=False):

    user_question: str

    origin: str
    destination: str

    start_date: str
    end_date: str
    dates_description: str

    budget: str
    preferences: str

    need_flights: bool
    need_hotels: bool
    need_web: bool
    need_weather: bool

    flight_results: str
    hotel_results: str
    research_results: str
    weather_results: str

    itinerary: str
    final_response: str


# =====================================================
# LLM
# =====================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)


# =====================================================
# RESEARCH PLAN
# =====================================================

class ResearchPlan(BaseModel):

    origin: str = ""
    destination: str = ""

    start_date: str = ""
    end_date: str = ""

    dates_description: str = ""

    budget: str = ""
    preferences: str = ""

    need_flights: bool = False
    need_hotels: bool = False
    need_web: bool = True
    need_weather: bool = True

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date(cls, value):

        if not value:
            return value

        parsed = date.fromisoformat(value)

        return parsed.isoformat()


# =====================================================
# CLEAN JSON
# =====================================================

def clean_json_response(text):

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s*```$", "", text)

    return text.strip()


# =====================================================
# PLANNER AGENT
# =====================================================

def research_planner_agent(state: AgentState):

    prompt = f"""
You are a professional travel planning agent.

Analyze the user's travel request.

Return ONLY valid JSON.

Use exactly these fields:

{{
    "origin": "",
    "destination": "",
    "start_date": "",
    "end_date": "",
    "dates_description": "",
    "budget": "",
    "preferences": "",
    "need_flights": false,
    "need_hotels": false,
    "need_web": true,
    "need_weather": true
}}

RULES:

1. Extract origin and destination.
2. Extract exact dates only when explicitly provided.
3. Never invent dates.
4. Dates must use YYYY-MM-DD.
5. Preserve natural-language dates in dates_description.
6. Extract budget.
7. Extract travel preferences.
8. Enable flights when the user requests flight searching.
9. Enable hotels when the user requests accommodation.
10. Enable web research for travel planning.
11. Enable weather when a destination is known.
12. Never assume missing information.

USER REQUEST:

{state["user_question"]}
"""

    try:

        response = llm.invoke(prompt)

        data = json.loads(
            clean_json_response(response.content)
        )

        plan = ResearchPlan.model_validate(data)

        state.update(plan.model_dump())

    except Exception as error:

        state.update({
            "origin": "",
            "destination": "",
            "start_date": "",
            "end_date": "",
            "dates_description": "",
            "budget": "",
            "preferences": "",
            "need_flights": False,
            "need_hotels": False,
            "need_web": True,
            "need_weather": True,
            "research_results": (
                f"Planner error: {str(error)}"
            )
        })

    return state
