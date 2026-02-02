from fastapi import Request, Header, HTTPException
from typing import Optional
from src.rate_limiter import check_rate_limit

async def get_rate_limiter(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    """
    Dependency to check rate limits.
    Identifies user tier and calls the rate limiter logic.
    """
    # Determine User Tier
    user_tier = "free"
    if x_api_key == "secret-pro-key":
        user_tier = "pro"
    
    # Identify Client
    # For Free users, use IP. For Pro users, use API Key.
    if user_tier == "pro":
        client_id = x_api_key
    else:
        client_id = request.client.host if request.client else "unknown"
        
    # Check Limit
    check_rate_limit(client_id, user_tier)
    
    return user_tier