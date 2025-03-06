import asyncio
import logging, json
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.orchestrators import MultiAgentOrchestrator
from modules.movie_recommendation_agent import MovieRecommendationAgent, search_latest_movies
from modules.movie_reservation_agent import MovieReservationAgent, book_movie
from modules.membership_agent import MembershipAgent, check_membership_status
from modules.config import get_llm_config, get_config
from modules.auth import get_token_provider
from modules.cache_config import get_cached_model_client

class MovieBookingOrchestrator:
    """Manages movie booking using AutoGen's `MultiAgentOrchestrator` for intelligent routing."""

    def __init__(self):
        # Initialize LLM Client
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

        # Initialize Agents
        self.movie_recommendation_agent = MovieRecommendationAgent()
        self.movie_reservation_agent = MovieReservationAgent()
        self.membership_agent = MembershipAgent()
        # Initialize other agents as needed
        # self.mobile_upgrade_agent = MobileUpgradeAgent()
        # self.membership_activation_agent = MembershipActivationAgent()
        # Add more agents here...

        # Define Assistant Agents
        self.recommendation_agent = AssistantAgent(
            "MovieRecommendationAgent",
            cached_client,
            tools=[search_latest_movies],
            description="Provides the latest movie recommendations."
        )

        self.reservation_agent = AssistantAgent(
            "MovieReservationAgent",
            cached_client,
            tools=[book_movie],
            description="Handles movie ticket reservations."
        )

        self.membership_agent_assistant = AssistantAgent(
            "MembershipAgent",
            cached_client,
            tools=[check_membership_status],
            description="Checks user membership and benefit eligibility."
        )

        # Define other Assistant Agents
        # self.mobile_upgrade_agent_assistant = AssistantAgent(
        #     "MobileUpgradeAgent",
        #     cached_client,
        #     tools=[upgrade_mobile_device],
        #     description="Handles mobile phone device upgrades."
        # )

        # self.membership_activation_agent_assistant = AssistantAgent(
        #     "MembershipActivationAgent",
        #     cached_client,
        #     tools=[activate_membership],
        #     description="Activates user membership."
        # )

        # Add more Assistant Agents here...

        # Define MultiAgentOrchestrator
        self.orchestrator = MultiAgentOrchestrator(
            agents=[
                self.recommendation_agent,
                self.reservation_agent,
                self.membership_agent_assistant,
                # self.mobile_upgrade_agent_assistant,
                # self.membership_activation_agent_assistant,
                # Add more Assistant Agents here...
            ],
            model_client=cached_client,
        )

    async def process_query(self, user_query: str, user_id: str):
        """Dynamically route user queries to the appropriate agent using `MultiAgentOrchestrator`."""

        logging.info(f"\nReceived query from User {user_id}: {user_query}")

        full_messages = []
        filtered_messages = []
        last_message = None

        async for msg in self.orchestrator.run_stream(task=f"User ID: {user_id}. {user_query}"):

            logging.debug(f" Raw Message Object: {msg}")

            if hasattr(msg, "content") and msg.content:
                if isinstance(msg.content, (list, dict)):
                    logging.debug(f"Skipping non-text content: {msg.content}")
                    continue

                full_messages.append(str(msg.content))
                filtered_messages.append(str(msg.content))
                last_message = msg.content

        full_response_log = "\n".join(full_messages)
        logging.info(f"AI Full Response Processed:\n{full_response_log}")

        return "\n".join(filtered_messages) if filtered_messages else "No response generated."











