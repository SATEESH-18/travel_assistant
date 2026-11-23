
---
title: AI Travel Assistant
emoji: ✈️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 6.32.0
app_file: app.py
pinned: false
---


# 🌍 AI Travel Assistant

An AI-powered multi-agent travel planning application built using Groq, LangChain, LangGraph, Duffel, LiteAPI, Tavily and OpenWeather.

## Project Overview

The AI Travel Assistant helps users plan personalized trips based on their origin, destination, dates, budget and travel preferences.

It uses a multi-agent architecture to collect travel information and generate practical itineraries.

## Features

- AI-powered travel planning
- Flight search using Duffel API
- Hotel search using LiteAPI
- Travel research using Tavily
- Current weather information using OpenWeather
- Personalized day-by-day itineraries
- Budget-aware travel recommendations
- Interactive Gradio user interface

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Groq | LLM inference |
| LangChain | LLM integration |
| LangGraph | Multi-agent workflow |
| Pydantic | Data validation |
| Gradio | User interface |
| Duffel | Flight search |
| LiteAPI | Hotel search |
| Tavily | Web research |
| OpenWeather | Weather information |

## Project Architecture

The application consists of the following agents:

1. Research Planner Agent
2. Flight Search Agent
3. Hotel Search Agent
4. Web Research Agent
5. Weather Agent
6. Itinerary Generation Agent
7. Final Response Agent

LangGraph coordinates the execution of these agents.

## Installation

Clone the repository:

```bash
git clone https://github.com/SATEESH-18/travel-assistant.git
cd travel-assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and configure your API keys.

Run the application:

```bash
python app.py
```

Open:

```text
[http://127.0.0.1:7860]
```

## Environment Variables

The application requires these API keys:

- GROQ_API_KEY
- DUFFEL_API_KEY
- LITEAPI_API_KEY
- TAVILY_API_KEY
- OPENWEATHER_API_KEY

Never commit your actual API keys to GitHub.

## Deployment

The application is designed for deployment using Hugging Face Spaces with the Gradio SDK.

Configure the required API keys as Hugging Face Space Secrets.

## Disclaimer

Flight and hotel results depend on third-party API responses, account permissions and availability. Weather information represents current conditions, not necessarily future forecasts.

## Author

Developed as an AI-powered multi-agent travel planning project.
