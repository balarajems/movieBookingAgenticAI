# modules/auth.py

from azure.identity import DefaultAzureCredential
from azure.core.credentials import AccessToken

def get_token_provider():
    """
    Returns a callable function that provides a Bearer token for Azure OpenAI.
    """
    def token_function():
        credential = DefaultAzureCredential()
        token: AccessToken = credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token

    return token_function
