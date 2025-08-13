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
