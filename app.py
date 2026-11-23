
import gradio as gr

from graph import run_travel_assistant


# =====================================================
# MAIN FUNCTION
# =====================================================

def generate_trip(
    origin,
    destination,
    start_date,
    end_date,
    budget,
    preferences,
    include_flights,
    include_hotels
):

    if not origin.strip():
        return "Please enter your departure city."

    if not destination.strip():
        return "Please enter your destination."

    if include_flights and not start_date:
        return "Please enter an exact departure date for flight search."

    if include_hotels and (not start_date or not end_date):
        return "Please enter check-in and check-out dates for hotel search."

    question = f"""
I want to travel from {origin} to {destination}.

Departure date: {start_date or "Not specified"}

Return date: {end_date or "Not specified"}

Budget: {budget or "Not specified"}

Preferences: {preferences or "No specific preferences"}

Please create a detailed travel itinerary.

Flight search requested: {include_flights}

Hotel search requested: {include_hotels}

Include food, cultural and technology experiences where relevant.
"""

    try:

        result = run_travel_assistant(question)

        return result

    except Exception as error:

        return f"An error occurred: {str(error)}"


# =====================================================
# GRADIO INTERFACE
# =====================================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI Travel Assistant"
) as demo:

    gr.Markdown(
        """
        # 🌍 AI Travel Assistant

        ### Plan your next journey with AI!

        Enter your travel details and receive a personalized
        travel itinerary with flight, hotel, weather and
        destination research.
        """
    )

    with gr.Row():

        origin = gr.Textbox(
            label="Origin",
            placeholder="Example: Delhi"
        )

        destination = gr.Textbox(
            label="Destination",
            placeholder="Example: Tokyo"
        )

    with gr.Row():

        start_date = gr.Textbox(
            label="Departure Date",
            placeholder="YYYY-MM-DD"
        )

        end_date = gr.Textbox(
            label="Return Date",
            placeholder="YYYY-MM-DD"
        )

    budget = gr.Textbox(
        label="Total Budget",
        placeholder="Example: ₹1,50,000"
    )

    preferences = gr.Textbox(
        label="Travel Preferences",
        placeholder="Food, technology, culture, shopping...",
        lines=3
    )

    gr.Markdown("### Select the services you need")

    with gr.Row():

        include_flights = gr.Checkbox(
            label="Search Flights",
            value=True
        )

        include_hotels = gr.Checkbox(
            label="Search Hotels",
            value=True
        )

    generate_button = gr.Button(
        "Generate My Travel Plan",
        variant="primary"
    )

    output = gr.Markdown(
        label="Your Travel Itinerary"
    )

    generate_button.click(
        fn=generate_trip,
        inputs=[
            origin,
            destination,
            start_date,
            end_date,
            budget,
            preferences,
            include_flights,
            include_hotels
        ],
        outputs=output
    )

    gr.Markdown(
        """
        ---
        **Powered by:** Groq | LangGraph | LangChain |
        Duffel | LiteAPI | Tavily | OpenWeather

        *Flight and hotel results depend on live API
        responses and account availability.*
        """
    )


# =====================================================
# LAUNCH APPLICATION
# =====================================================

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
