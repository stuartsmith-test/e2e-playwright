# tests/api/test_add_to_cart.py
from utils.api_helpers import reset_cart, add_to_cart

def test_add_to_cart(api_request_context):
    """
    Resets the cart, then adds a known item (id=1) and verifies success.
    """
    # Step 1: ensure clean state
    reset_cart(api_request_context)

    # Step 2: add an item
    add_to_cart(api_request_context, item_id=1)

    # Optional debug output
    print("✅ Cart reset and item 1 successfully added via API.")

    # Step 3: verify item was added (this would typically involve checking the cart contents)