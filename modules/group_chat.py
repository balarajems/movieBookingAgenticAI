import asyncio
import logging, json
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from modules.movie_recommendation_agent import MovieRecommendationAgent, search_latest_movies
from modules.movie_reservation_agent import MovieReservationAgent, book_movie
from modules.membership_agent import MembershipAgent, check_membership_status
from modules.config import get_llm_config, get_config
from modules.auth import get_token_provider
from modules.cache_config import get_cached_model_client

class MovieBookingGroupChat:
    """Manages movie booking using AutoGen's `SelectorGroupChat` for intelligent routing."""

    def __init__(self):
        #  Initialize LLM Client
        config = get_config()

        # Get the Bearer token provider
        token_provider = get_token_provider()

        # Initialize AzureOpenAIChatCompletionClient
        model_client = AzureOpenAIChatCompletionClient(
            azure_deployment=config['AZURE_OPENAI_DEPLOYMENT_ID'],
            model=config['AZURE_OPENAI_MODEL_NAME'],
            api_version=config['AZURE_OPENAI_API_VERSION'],
            azure_endpoint=config['AZURE_OPENAI_ENDPOINT'],
            azure_ad_token_provider=token_provider,  # Pass the callable function
        )

        cached_client = get_cached_model_client(model_client)

        #  Initialize Agents
        self.movie_recommendation_agent = MovieRecommendationAgent()
        self.movie_reservation_agent = MovieReservationAgent()
        self.membership_agent = MembershipAgent()

        #  Define Assistant Agents
        self.recommendation_agent = AssistantAgent(
            "MovieRecommendationAgent",
            cached_client,
            tools=[search_latest_movies],  # Tool-based function
            description="Provides the latest movie recommendations."
        )

        self.reservation_agent = AssistantAgent(
            "MovieReservationAgent",
            cached_client,
            tools=[book_movie],  # Calls booking API
            description="Handles movie ticket reservations."
        )

        self.membership_agent_assistant = AssistantAgent(
            "MembershipAgent",
            cached_client,
            tools=[check_membership_status],  # Auto-verifies membership
            description="Checks user membership and benefit eligibility."
        )

        #  Define `SelectorGroupChat`
        self.team = SelectorGroupChat(
            [self.recommendation_agent, self.reservation_agent, self.membership_agent_assistant],
            model_client=cached_client,
            termination_condition=TextMentionTermination("TERMINATE"),
        )

    async def process_query(self, user_query: str, user_id: str):
        """Dynamically route user queries to the appropriate agent using `SelectorGroupChat`."""

        logging.info(f"\nReceived query from User {user_id}: {user_query}")

        full_messages = []  # Store all messages for final user output
        filtered_messages = []  # Messages excluding lists/dicts
        last_message = None  # Store the final AI response

        async for msg in self.team.run_stream(task=f"User ID: {user_id}. {user_query}"):

            # Log full raw response for debugging
            logging.debug(f" Raw Message Object: {msg}")

            if hasattr(msg, "content") and msg.content:
                # Store only text responses and ignore JSON lists/dicts
                if isinstance(msg.content, (list, dict)):
                    logging.debug(f"Skipping non-text content: {msg.content}")
                    continue  

                # Capture all valid text responses
                full_messages.append(str(msg.content))  
                filtered_messages.append(str(msg.content))  
                last_message = msg.content  # Capture last human-readable response

        # Log the full conversation, including all relevant responses
        full_response_log = "\n".join(full_messages)
        logging.info(f"AI Full Response Processed:\n{full_response_log}")

        # Return the full filtered AI response for the user
        return "\n".join(filtered_messages) if filtered_messages else "No response generated."











