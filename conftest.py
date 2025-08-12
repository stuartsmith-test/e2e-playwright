#conftest.py
#this file holds fixtures available to all tests
import pytest
from typing import Generator
from playwright.sync_api import APIRequestContext, Playwright

"""Create and manage a Playwright API request context for tests.

This fixture provides a shared API request context that can be used across tests
during a test session. It handles creation and cleanup of the context.

Args:
    playwright (Playwright): The Playwright instance
    base_url (str): The base URL to use for requests from pytest-base-url

Yields:
    APIRequestContext: A Playwright API request context configured with the base URL

Note:
    The context is automatically disposed after all tests complete
"""
@pytest.fixture(scope="session") 
def api_request_context(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """Shared Playwright API client using pytest-base-url's base_url."""
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
