import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class RateLimitEntry:
    request_count: int
    window_start_time: float

class RateLimitExceeded(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after

# Global in-memory store
# Key: Client Identifier (IP or API Key)
# Value: RateLimitEntry
rate_limit_store: Dict[str, RateLimitEntry] = {}

WINDOW_SIZE_SECONDS = 60
LIMIT_FREE = 5
LIMIT_PRO = 100

def check_rate_limit(client_id: str, user_tier: str):
    """
    Check if the client has exceeded the rate limit using the Fixed Window algorithm.
    
    Args:
        client_id (str): Unique identifier for the client (IP or API Key).
        user_tier (str): The tier of the user ('free' or 'pro').
        
    Raises:
        RateLimitExceeded: If the request count exceeds the limit for the current window.
    """
    current_time = time.time()
    limit = LIMIT_PRO if user_tier == "pro" else LIMIT_FREE
    
    if client_id not in rate_limit_store:
        rate_limit_store[client_id] = RateLimitEntry(
            request_count=1,
            window_start_time=current_time
        )
        return

    entry = rate_limit_store[client_id]
    
    # Check if window has expired
    if current_time - entry.window_start_time > WINDOW_SIZE_SECONDS:
        # Reset window
        entry.request_count = 1
        entry.window_start_time = current_time
        return

    # Check limit
    if entry.request_count >= limit:
        retry_after = int(WINDOW_SIZE_SECONDS - (current_time - entry.window_start_time))
        raise RateLimitExceeded(retry_after=retry_after)

    # Increment count
    entry.request_count += 1