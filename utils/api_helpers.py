# utils/api_helpers.py
"""Helpers for interacting with cart-related API endpoints in Playwright tests.

These helpers accept Playwright's `APIRequestContext`, which is the same type used to
perform HTTP requests in tests. There are two typical ways you will obtain an
`APIRequestContext`:

1. API tests: use the `api_request_context` fixture provided by the Playwright
   test runner. Example:

       reset_cart(api_request_context)

2. UI tests: access the request context off a `Page` instance via `page.request`.
   Example:

       reset_cart(page.request)

Both values implement the same interface and work identically with these helpers.
Centralizing common actions here ensures consistent status assertions and request
shapes across all tests.
"""

# Third‑party: Playwright types for request + response objects
from playwright.sync_api import APIRequestContext, APIResponse


def reset_cart(api_request_context: APIRequestContext) -> APIResponse:
    """
    Clear the cart using POST /reset-cart.

    Args:
        api_request_context (APIRequestContext): Playwright API request context.

    Returns:
        APIResponse: The Playwright response object for optional debugging.

    Raises:
        AssertionError: If the response status is not OK.
    """
    response = api_request_context.post("/reset-cart")
    assert response.ok, f"Reset cart failed. Status: {response.status}"
    return response


def add_to_cart(api_request_context: APIRequestContext, item_id: int) -> APIResponse:
    """
    Add a single item to the cart via POST /add-to-cart.

    Args:
        api_request_context (APIRequestContext): Playwright API request context.
        item_id (int): ID of the item to add.

    Returns:
        APIResponse: The Playwright response object for optional debugging.

    Raises:
        AssertionError: If the response status is not OK.
    """
    response = api_request_context.post("/add-to-cart", data={"itemId": item_id})
    assert response.ok, f"Add to cart failed. Status: {response.status}"
    return response
