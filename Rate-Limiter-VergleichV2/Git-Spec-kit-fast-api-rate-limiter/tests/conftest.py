import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.rate_limiter import rate_limit_store
import time
from unittest.mock import patch

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_rate_limit_store():
    """Clear the rate limit store before each test."""
    rate_limit_store.clear()
    yield

@pytest.fixture
def mock_time():
    """Mock time.time() to return a controlled value."""
    with patch("src.rate_limiter.time.time") as mock_time:
        mock_time.return_value = 1000.0  # Start at a fixed time
        yield mock_time