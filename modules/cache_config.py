# modules/cache_config.py

import os
from diskcache import Cache
from autogen_ext.models.cache import ChatCompletionCache, CHAT_CACHE_VALUE_TYPE
from autogen_ext.cache_store.diskcache import DiskCacheStore

# Define Cache Directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), '../cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Use DiskCacheStore for persistent local caching
cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache(CACHE_DIR))

def get_cached_model_client(model_client):
    """Wraps a model client with caching."""
    return ChatCompletionCache(model_client, cache_store)
