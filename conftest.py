# conftest.py
"""Global pytest fixtures available to all tests.

Currently provides:
- `api_request_context`: a shared Playwright API client configured with pytest-base-url.
"""

import pytest  # pytest fixture decorator and scopes
from typing import Generator  # precise type for a yielding fixture
from playwright.sync_api import APIRequestContext, Playwright  # Playwright types used by the fixture


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright, base_url: str
) -> Generator[APIRequestContext, None, None]:
    """Provide a Playwright API client scoped to the entire test session.

    Creates an APIRequestContext preconfigured with the pytest-base-url `base_url`.
    Ensures proper cleanup after all tests complete.

    Args:
        playwright: The Playwright instance.
        base_url: Base URL from pytest-base-url plugin.

    Yields:
        APIRequestContext: Playwright API client.
    """
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
