
from langgraph.graph import StateGraph, START, END

from agents.planner import (
    AgentState,
    research_planner_agent
)

from tools.flights import flight_search_agent
from tools.hotels import hotel_search_agent
from tools.web_search import web_search_agent
from tools.weather import weather_search_agent

from agents.itinerary import (
    itinerary_agent,
    final_llm_agent
)


# =====================================================
# DISPATCHER
# =====================================================

def research_dispatcher(state):

    return state


# =====================================================
# SELECT FIRST NODE
# =====================================================

def choose_first_research_node(state):

    if state.get("need_flights"):
        return "flight_search"

    if state.get("need_hotels"):
        return "hotel_search"

    if state.get("need_web"):
        return "web_search"

    if state.get("need_weather"):
        return "weather_search"

    return "itinerary"


# =====================================================
# ROUTING AFTER FLIGHTS
# =====================================================

def after_flight(state):

    if state.get("need_hotels"):
        return "hotel_search"

    if state.get("need_web"):
        return "web_search"

    if state.get("need_weather"):
        return "weather_search"

    return "itinerary"


# =====================================================
# ROUTING AFTER HOTELS
# =====================================================

def after_hotel(state):

    if state.get("need_web"):
        return "web_search"

    if state.get("need_weather"):
        return "weather_search"

    return "itinerary"


# =====================================================
# ROUTING AFTER WEB
# =====================================================

def after_web(state):

    if state.get("need_weather"):
        return "weather_search"

    return "itinerary"


# =====================================================
# BUILD GRAPH
# =====================================================

graph = StateGraph(AgentState)


# Add nodes

graph.add_node(
    "research_planner",
    research_planner_agent
)

graph.add_node(
    "research_dispatcher",
    research_dispatcher
)

graph.add_node(
    "flight_search",
    flight_search_agent
)

graph.add_node(
    "hotel_search",
    hotel_search_agent
)

graph.add_node(
    "web_search",
    web_search_agent
)

graph.add_node(
    "weather_search",
    weather_search_agent
)

graph.add_node(
    "itinerary",
    itinerary_agent
)

graph.add_node(
    "final_llm",
    final_llm_agent
)


# =====================================================
# CONNECT NODES
# =====================================================

graph.add_edge(
    START,
    "research_planner"
)

graph.add_edge(
    "research_planner",
    "research_dispatcher"
)


# Conditional routing

graph.add_conditional_edges(
    "research_dispatcher",
    choose_first_research_node
)

graph.add_conditional_edges(
    "flight_search",
    after_flight
)

graph.add_conditional_edges(
    "hotel_search",
    after_hotel
)

graph.add_conditional_edges(
    "web_search",
    after_web
)


# Weather leads to itinerary

graph.add_edge(
    "weather_search",
    "itinerary"
)


# Itinerary leads to final response

graph.add_edge(
    "itinerary",
    "final_llm"
)

graph.add_edge(
    "final_llm",
    END
)


# =====================================================
# COMPILE
# =====================================================

app = graph.compile()


def run_travel_assistant(user_question: str):

    initial_state = {
        "user_question": user_question,
        "flight_results": "",
        "hotel_results": "",
        "research_results": "",
        "weather_results": "",
        "itinerary": "",
        "final_response": ""
    }

    result = app.invoke(
        initial_state
    )

    return result.get(
        "final_response",
        "Sorry, I could not generate a travel plan."
    )
