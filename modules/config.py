# modules/config.py
# modules/config.py

import os
import logging
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Configure Logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_config():
    """Retrieve API configuration."""
    return {
        "MOVIE_BOOKING_API_URL": os.getenv("MOVIE_BOOKING_API_URL"),
        "MOVIE_BOOKING_API_KEY": os.getenv("MOVIE_BOOKING_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_MODEL_NAME": os.getenv("AZURE_OPENAI_MODEL_NAME"),
        "AZURE_OPENAI_DEPLOYMENT_ID": os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
        "BING_SEARCH_API_KEY": os.getenv("BING_SEARCH_API_KEY"),
        "SEMANTIC_KERNEL_FUNCTION_URL": "https://telecom-sk-function.azurewebsites.net"
    }


config = get_config()

def get_llm_config():
    return {
        "config_list": [
            {
                "api_type": "azure",
                "base_url": config['AZURE_OPENAI_ENDPOINT'],
                "api_version": config['AZURE_OPENAI_API_VERSION'],
                "api_key": config['AZURE_OPENAI_API_KEY'],
                "model": config['AZURE_OPENAI_MODEL_NAME'],
            }
        ]
    }