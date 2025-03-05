# modules/membership_agent.py

from typing import Annotated
from autogen import ConversableAgent
from modules.config import get_llm_config
from modules.config import get_config
import logging


async def check_membership_status( 
    user_id: Annotated[str, "The user's unique membership ID."]
) -> Annotated[str, "Membership verification result"]:
    """Checks if a user is eligible for booking benefits."""
    logging.info(f"Checking membership status for User ID: {user_id}")

    # Mocked membership data (Replace with real API call later)
    mock_membership_db = {
        "12345": {"status": "active", "level": "premium"},
        "67890": {"status": "inactive", "level": "basic"},
        "99999": {"status": "expired", "level": "basic"},
    }

    membership_info = mock_membership_db.get(user_id, {"status": "unknown"})

    # Return structured eligibility response
    if membership_info["status"] == "active":
        return {"message": "eligible", "membership_level": membership_info["level"]}
    else:
        return {"message": "not eligible", "error": "User does not have an active membership."}

class MembershipAgent:
    """Agent responsible for checking user membership status before booking."""

    def __init__(self):
        llm_config = get_llm_config()
        config = get_config()

        # Store Membership API URL
        self.membership_api_url = f"{config['SEMANTIC_KERNEL_FUNCTION_URL']}/api/MembershipVerificationPlugin"

        # Define Membership Agent
        self.agent = ConversableAgent(
            name="MovieRecommendationAgent",
            system_message=(
                "You recommend movies based on the user's preference. "
                "When the user asks for movies of a certain genre (e.g., 'action movie'), "
                "IMMEDIATELY call `search_latest_movies` with the correct genre."
            ),
            llm_config=llm_config
        )
