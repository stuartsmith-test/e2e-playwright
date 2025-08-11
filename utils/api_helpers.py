# utils/api_helpers.py
""" API helper functions for cart management in e-commerce testing.
This module provides utility functions to interact with cart-related API endpoints,
specifically for resetting the cart and adding items to it.
Functions:
    reset_cart(api_request_context: APIRequestContext) -> None:
        Sends a POST request to clear all items from the cart.
    add_to_cart(api_request_context: APIRequestContext, item_id: int) -> None:
        Sends a POST request to add a specific item to the cart.
Args:
    api_request_context: Playwright's API request context for making HTTP calls
    item_id: Integer ID of the item to be added to cart
Raises:
    AssertionError: If any API request fails (non-OK response)
Example:
    api_context = playwright.request.new_context()
    reset_cart(api_context)
    add_to_cart(api_context, 12345) """
from playwright.sync_api import APIRequestContext

def reset_cart(api_request_context: APIRequestContext) -> None:
    """
    Clear the cart using POST /reset-cart.
    Raises an assertion error on failure.
    """
    response = api_request_context.post("/reset-cart")
    assert response.ok, f"Reset cart failed. Status: {response.status}"

def add_to_cart(api_request_context: APIRequestContext, item_id: int) -> None:
    """
    Add a single item to the cart via POST /add-to-cart.
    Raises an assertion error on failure.
    """
    response = api_request_context.post("/add-to-cart", data={"itemId": item_id})
    assert response.ok, f"Add to cart failed. Status: {response.status}"
