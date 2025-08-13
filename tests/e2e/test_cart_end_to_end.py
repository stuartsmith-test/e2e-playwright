# tests/e2e/test_cart_end_to_end.py
"""E2E (API → DB → UI): prove add-to-cart persists and is visible in the UI.

Flow:
1) Reset cart via API
2) Add the same item twice via API
3) Assert DB quantity == 2
4) Assert /cart shows quantity == 2 for that item
"""

from playwright.sync_api import Page, APIRequestContext  # Playwright page + API context
from utils.api_helpers import reset_cart, add_to_cart  # API helpers
from utils import dbHelpers as db  # DB read helpers for assertions


def test_cart_quantity_reflects_api_and_db(
    page: Page, base_url: str, api_request_context: APIRequestContext
) -> None:
    """End-to-end check that ties API action → DB state → UI rendering."""
    item_id = 1

    # Arrange: ensure clean slate
    reset_cart(api_request_context)
    start_qty = db.get_cart_quantity(item_id)
    print(f"[DEBUG] Start quantity for item {item_id}: {start_qty}")
    assert start_qty == 0, "Expected empty cart at test start"

    # Use DB to resolve a robust UI locator (item name)
    item_name = db.get_item_name(item_id)
    assert item_name, f"Item id {item_id} not found in DB; cannot locate on UI"
    print(f"[DEBUG] Item {item_id} resolves to name: {item_name!r}")

    # Act: add twice via API
    r1 = add_to_cart(api_request_context, item_id)
    print(f"[DEBUG] First add status: {r1.status}")
    r2 = add_to_cart(api_request_context, item_id)
    print(f"[DEBUG] Second add status: {r2.status}")

    # Assert (DB): quantity is 2
    qty = db.get_cart_quantity(item_id)
    print(f"[DEBUG] DB quantity after adds: {qty}")
    assert qty == 2, f"Expected quantity 2 for item {item_id}, got {qty}"

    # Assert (UI): /cart shows quantity=2 for this item
    page.goto(f"{base_url}/cart")
    page.wait_for_url("**/cart")
    page.wait_for_load_state("domcontentloaded")

    # Accessible row name includes "<item> 2 $" in this app
    row = page.get_by_role("row", name=f"{item_name} 2 $")
    form_locator = row.locator("form")
    assert form_locator.is_visible(), f"Expected quantity 2 for {item_name} on /cart"

    # Cleanup
    reset_cart(api_request_context)
    print("[DEBUG] Cleanup done (cart reset).")
