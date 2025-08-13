# utils/api_helpers.py
"""Helpers for interacting with cart-related API endpoints in Playwright tests."""

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
