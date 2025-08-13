# tests/e2e/test_cart_db_validation.py
"""E2E (API → DB) validation.

Proves that POST /add-to-cart updates the SQLite `cart` table:
- Reset cart via API
- Add the same item twice via API
- Assert DB quantity == 2
- Reset cart to clean up

This test focuses on persisted state (DB). UI checks live in UI/E2E tests.
"""

from playwright.sync_api import APIRequestContext  # fixture type hint for readability
from utils.api_helpers import reset_cart, add_to_cart  # API helpers (assert on status)
from utils import dbHelpers as db  # DB read helpers


def test_add_to_cart_updates_db(api_request_context: APIRequestContext) -> None:
    """Adding an item twice via API should persist quantity=2 in the DB."""
    item_id = 1

    # Arrange: ensure clean start
    reset_cart(api_request_context)
    start_qty = db.get_cart_quantity(item_id)
    print(f"[DEBUG] Start quantity for item {item_id}: {start_qty}")
    assert start_qty == 0, "Cart not empty at test start"

    # Act: add the same item twice via API
    resp1 = add_to_cart(api_request_context, item_id)
    print(f"[DEBUG] First add status: {resp1.status}")
    resp2 = add_to_cart(api_request_context, item_id)
    print(f"[DEBUG] Second add status: {resp2.status}")

    # Assert: DB reflects the expected persisted quantity
    qty = db.get_cart_quantity(item_id)
    print(f"[DEBUG] DB quantity after adds: {qty}")
    assert qty == 2, f"Expected quantity 2 for item {item_id}, got {qty}"

    # Cleanup
    reset_cart(api_request_context)
    print("[DEBUG] Cleanup done (cart reset).")
