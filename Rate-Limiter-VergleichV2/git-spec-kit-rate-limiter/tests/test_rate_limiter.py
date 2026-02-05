import pytest
from src.rate_limiter import check_rate_limit, RateLimitExceeded, rate_limit_store
from fastapi.testclient import TestClient

def test_free_user_rate_limit_logic(mock_time):
    """
    Test that a free user is limited to 5 requests per minute.
    """
    client_id = "127.0.0.1"
    
    # 5 allowed requests
    for _ in range(5):
        check_rate_limit(client_id, "free")
    
    # 6th request should raise exception
    with pytest.raises(RateLimitExceeded) as excinfo:
        check_rate_limit(client_id, "free")
    
    # Retry-After should be 60 seconds (since we are at start of window)
    assert excinfo.value.retry_after == 60

def test_free_user_window_reset(mock_time):
    """
    Test that the window resets after 60 seconds.
    """
    client_id = "127.0.0.1"
    
    # Consume limit
    for _ in range(5):
        check_rate_limit(client_id, "free")
        
    # Advance time by 61 seconds
    mock_time.return_value += 61
    
    # Should be allowed again
    check_rate_limit(client_id, "free")

def test_integration_free_user_limit(client):
    """
    Integration test for the /analyze endpoint.
    """
    payload = {"text": "test"}
    
    # 5 allowed requests
    for _ in range(5):
        response = client.post("/analyze", json=payload)
        assert response.status_code == 200
        
    # 6th request should be 429
    response = client.post("/analyze", json=payload)
    assert response.status_code == 429
    assert "Retry-After" in response.headers

def test_pro_user_rate_limit_logic(mock_time):
    """
    Test that a pro user is limited to 100 requests per minute.
    """
    client_id = "secret-pro-key"
    
    # 100 allowed requests
    for _ in range(100):
        check_rate_limit(client_id, "pro")
    
    # 101st request should raise exception
    with pytest.raises(RateLimitExceeded):
        check_rate_limit(client_id, "pro")

def test_integration_pro_user_limit(client):
    """
    Integration test for the /analyze endpoint with Pro Key.
    """
    payload = {"text": "test"}
    headers = {"x-api-key": "secret-pro-key"}
    
    # 100 allowed requests
    for _ in range(100):
        response = client.post("/analyze", json=payload, headers=headers)
        assert response.status_code == 200
        
    # 101st request should be 429
    response = client.post("/analyze", json=payload, headers=headers)
    assert response.status_code == 429

def test_rate_limit_response_structure(client):
    """
    Test that the 429 response contains the correct headers and body.
    """
    payload = {"text": "test"}
    
    # Trigger rate limit
    for _ in range(6):
        response = client.post("/analyze", json=payload)
        
    assert response.status_code == 429
    assert "Retry-After" in response.headers
    assert response.json() == {"detail": "Rate limit exceeded"}
    
    # Verify Retry-After is an integer
    retry_after = int(response.headers["Retry-After"])
    assert retry_after > 0
    assert retry_after <= 60