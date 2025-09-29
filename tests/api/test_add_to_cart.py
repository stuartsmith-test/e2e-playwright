# tests/api/test_add_to_cart.py
"""API smoke test: verify POST /add-to-cart succeeds for a known item.

This file focuses on the HTTP contract (status/redirect). It does NOT assert DB or UI state.
Those are covered in dedicated API→DB and API→DB→UI tests.
"""

from playwright.sync_api import APIRequestContext  # fixture type hint for clarity in IDEs
from utils.api_helpers import reset_cart, add_to_cart  # small wrappers that assert status codes


def test_add_to_cart(api_request_context: APIRequestContext) -> None:
    """Reset the cart, add item id=1, and expect a successful server response.

    Notes:
        - Helpers (`reset_cart`, `add_to_cart`) perform the status assertions internally.
        - Cart state validation is exercised in `tests/e2e/test_cart_db_validation.py`.
    """
    # Step 1: ensure clean state (Arrange)
    reset_cart(api_request_context)

    # Step 2: add an item (Act)
    add_to_cart(api_request_context, item_id=1)

    # Step 3: (Assert) done implicitly by helpers. Keep lightweight on purpose.
    print("✅ API-only: cart reset and item 1 added successfully.")


def test_add_invalid_item_id(api_request_context: APIRequestContext) -> None:
    """Verify that adding an invalid item ID returns an appropriate error response.

    This test ensures the API properly handles invalid input by:
    1. Resetting the cart to a known state
    2. Attempting to add a non-existent item ID
    3. Verifying the API returns an error status code
    """
    # Step 1: ensure clean state
    reset_cart(api_request_context)

    # Step 2: attempt to add invalid item
    response = api_request_context.post("/add-to-cart", data={
        "item_id": 99999  # assuming this ID doesn't exist
    })

    # Step 3: verify error response
    assert response.status == 400, f"Expected 400 status, got {response.status}"
    error_data = response.json()
    assert "error" in error_data, "Response should contain error message"
    print("✅ API-only: invalid item ID properly rejected")


def test_add_multiple_items(api_request_context: APIRequestContext) -> None:
    """Verify that multiple items can be added to the cart successfully.

    This test ensures the API can handle sequential item additions by:
    1. Resetting the cart to a known state
    2. Adding multiple different items
    3. Verifying each addition succeeds
    """
    # Step 1: ensure clean state
    reset_cart(api_request_context)

    # Step 2: add multiple items
    test_items = [1, 2, 3]  # assuming these are valid item IDs
    for item_id in test_items:
        add_to_cart(api_request_context, item_id=item_id)

    print("✅ API-only: multiple items added successfully")


def test_add_invalid_quantity(api_request_context: APIRequestContext) -> None:
    """Verify that adding items with invalid quantities is properly handled.

    Tests both negative and zero quantities to ensure the API:
    1. Rejects negative quantities
    2. Rejects zero quantities
    3. Returns appropriate error responses
    """
    # Step 1: ensure clean state
    reset_cart(api_request_context)

    # Step 2: test negative quantity
    response = api_request_context.post("/add-to-cart", data={
        "item_id": 1,
        "quantity": -1
    })
    assert response.status == 400, f"Expected 400 status for negative quantity, got {response.status}"
    
    # Step 3: test zero quantity
    response = api_request_context.post("/add-to-cart", data={
        "item_id": 1,
        "quantity": 0
    })
    assert response.status == 400, f"Expected 400 status for zero quantity, got {response.status}"

    print("✅ API-only: invalid quantities properly rejected")
