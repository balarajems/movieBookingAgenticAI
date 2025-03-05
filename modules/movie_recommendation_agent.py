# modules/movie_recommendation_agent.py

from typing import Annotated, Dict, List
from autogen import ConversableAgent, register_function
import requests
from modules.config import get_llm_config
from modules.config import get_config
import logging


async def search_latest_movies( 
) -> Annotated[dict, "List of recommended movies"]:
    """Calls Bing Search API to fetch trending movies."""
    logging.info(f" Mocking latest movies search for query:")

    # Simulated movie list (mocked response)
    mock_movies = [
        "Inception",
        "Dune: Part Two",
        "Spider-Man: Across the Spider-Verse",
        "Oppenheimer",
        "The Batman"
    ]
    
    logging.info(f" Mocked Movies Found: {mock_movies}")

    return {"movies": mock_movies}  # Returning fake results instead of Bing API

class MovieRecommendationAgent:
    """Fetches latest movies using Bing Search API."""

    def __init__(self):
        llm_config = get_llm_config()
        config = get_config()

        # Store Bing Search API Key
        # self.bing_api_key = config["BING_SEARCH_API_KEY"]
        # self.bing_api_url = "https://api.bing.microsoft.com/v7.0/search"

        # Define Movie Recommendation Agent
        self.agent = ConversableAgent(
            name="MovieRecommendationAgent",
            system_message=(
                "You are an expert in recommending movies to users. "
                "If a user asks for movie recommendations, you must call the function `search_latest_movies`. "
                "If the user provides a genre (e.g., 'action', 'comedy'), pass it as an argument."
            ),
            llm_config=llm_config
        )

        # Register function for LLM usage (LLM knows this function exists)
        self.agent.register_for_llm(
            name="search_latest_movies",
            description="Searches for the latest trending movies."
        )(search_latest_movies)

        # Register function for execution (MovieRecommendationAgent executes it)
        self.agent.register_for_execution(
            name="search_latest_movies"
        )(search_latest_movies)
    

    # def search_latest_movies(self, query="latest movies"):
    #     """Calls Bing Search API to fetch trending movies."""
    #     logging.info(f"🔍 Fetching latest movies with query: {query}")

    #     headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
    #     params = {"q": query, "count": 5}

    #     try:
    #         response = requests.get(self.bing_api_url, headers=headers, params=params)
    #         response.raise_for_status()
    #         results = response.json()

    #         # Extract movie titles from search results
    #         movies = [item["name"] for item in results.get("webPages", {}).get("value", [])]
    #         logging.info(f"🎬 Movies found: {movies}")

    #         return {"movies": movies} if movies else {"movies": ["No recent movies found."]}

    #     except requests.exceptions.RequestException as e:
    #         logging.error(f"❌ Movie search failed: {e}")
    #         return {"error": "Movie search service unavailable"}