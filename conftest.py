#conftest.py
#this file holds fixtures available to all tests
import os
import pytest
from typing import Generator
from playwright.sync_api import APIRequestContext, Playwright
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


"""
Fixture providing a Playwright API request context for making HTTP requests.
This fixture creates and yields a Playwright APIRequestContext configured with a base URL
from environment variables. The context is automatically disposed after use.
Args:
    playwright (Playwright): The Playwright instance provided by pytest-playwright
Returns:
    APIRequestContext: A context object for making API requests with shared base URL
Raises:
    ValueError: If BASE_URL environment variable is not set
Example:
    def test_api(api_request_context):
        response = api_request_context.get("/endpoint")
"""
@pytest.fixture(scope="session") 
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL is not set in environment variables.")
    
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
