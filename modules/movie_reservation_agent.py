# modules/movie_reservation_agent.py

from typing import Annotated
from autogen import ConversableAgent
from pydantic import BaseModel, Field
from modules.config import get_llm_config, get_config
from modules.membership_agent import MembershipAgent
import asyncio, logging, requests



# async def book_movie(
#     movie_title: Annotated[str, "The movie the user wants to book."],
#     user_id: Annotated[str, "User ID for membership verification."]
# ) -> Annotated[str, "Booking confirmation message"]:
#     """Processes a movie booking request."""
#     logging.info(f"🎟 Booking request received for {movie_title} by User ID: {user_id}")

#     # 🔹 Step 1: AutoGen will now call `check_membership_status` automatically before proceeding!

#     # 🔹 Step 2: If AutoGen determines eligibility, proceed with booking
#     booking_payload = {
#         "user_id": user_id,
#         "movie_title": movie_title,
#     }


        # Store Movie Booking API details
        # movie_booking_api_url = config["MOVIE_BOOKING_API_URL"]
        # movie_booking_api_key = config["MOVIE_BOOKING_API_KEY"]

#     try:
#         response = requests.post(movie_booking_api_url, json=booking_payload)
#         response.raise_for_status()
#         booking_data = response.json()

#         logging.info(f"Booking API Response: {booking_data}")
#         return booking_data

#     except requests.exceptions.RequestException as e:
#         logging.error(f"❌ Movie booking failed: {e}")
#         return {"error": "Movie booking service unavailable"}

class BookMovieParams(BaseModel):
    user_id: str = Field(..., description="The unique identifier of the user")
    movie_title: str = Field(..., description="The title of the movie the user wants to book")
    showtime: str = Field(..., description="The preferred showtime for the movie, e.g., '7:00 PM'")


async def book_movie(
params: BookMovieParams
) -> str:
    """Simulates a successful movie booking instead of calling a real API."""

    logging.info(f"Mock booking for user {params.user_id}: {params.movie_title} at {params.showtime}")

    # Simulate API delay
    await asyncio.sleep(1)

    # Simulated response
    return f"🎉 Success! Your ticket for '{params.movie_title}' at {params.showtime} has been booked. Enjoy your movie! 🎬"


class MovieReservationAgent:
    """Handles movie reservations, ensuring membership verification is done automatically."""

    def __init__(self):
        llm_config = get_llm_config()
        config = get_config()

        # Define Reservation Agent
        self.agent = ConversableAgent(
            name="MovieReservationAgent",
            system_message=(
                "You book movies for users. "
                "Before booking, check membership eligibility using the `check_membership_status` function."
                "If the user is eligible, proceed with booking. Otherwise, do not book the movie."
            ),
            llm_config=llm_config
        )


        # Register function for LLM usage (LLM knows this function exists)
        self.agent.register_for_llm(
            name="book_movie",
            description="Book movies for users"
        )(book_movie)

        # Register function for execution (MovieRecommendationAgent executes it)
        self.agent.register_for_execution(
            name="book_movie"
        )(book_movie)
