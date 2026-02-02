import pytest
from fastapi.testclient import TestClient
from src.main import app, expensive_computation
from unittest.mock import patch

client = TestClient(app)

# Mock expensive_computation to speed up tests
@pytest.fixture(autouse=True)
def mock_expensive_computation():
    with patch("src.main.expensive_computation"):
        yield

def test_rate_limit_free_user():
    # Reset limiter storage for this test (if possible, or rely on fresh start)
    # Since we can't easily reset the internal state of the global limiter without accessing private members,
    # we will rely on the fact that tests might run in order or we just test the limit directly.
    # A better way for robust tests is to mock the IP or clear storage.
    
    # Let's try to clear storage manually if we can, or just proceed.
    # For simple script execution, it starts fresh.
    
    # Free user limit is 5 per minute
    for i in range(5):
        response = client.post(
            "/analyze",
            json={"text": "test"},
            headers={"x-api-key": "free-key"} # or no key
        )
        assert response.status_code == 200, f"Request {i+1} failed for free user"

    # 6th request should fail
    response = client.post(
        "/analyze",
        json={"text": "test"},
        headers={"x-api-key": "free-key"}
    )
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text

def test_rate_limit_pro_user():
    # We need a way to reset the limit or use a different "user" (IP)
    # TestClient sends requests from 'testclient' host by default.
    # We can mock the remote address to simulate a different user.
    
    with patch("src.main.get_remote_address", return_value="127.0.0.2"):
        # Pro user limit is 100 per minute
        for i in range(100):
            response = client.post(
                "/analyze",
                json={"text": "test"},
                headers={"x-api-key": "secret-pro-key"}
            )
            assert response.status_code == 200, f"Request {i+1} failed for pro user"

        # 101st request should fail
        response = client.post(
            "/analyze",
            json={"text": "test"},
            headers={"x-api-key": "secret-pro-key"}
        )
        assert response.status_code == 429