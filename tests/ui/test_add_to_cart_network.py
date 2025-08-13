# tests/ui/test_add_to_cart_network.py
"""
UI + Network test:
Validates that clicking "Add to cart" in the UI sends the expected backend request.

Flow:
1. Reset cart via API to start with clean state
2. Navigate to homepage
3. Locate and verify visibility of the form for item_id=1
4. Click the button while capturing the network request/response
5. Assert correct HTTP method, payload, and a success/redirect status code
"""

from utils.api_helpers import reset_cart  # API cleanup
from utils.ui_helpers import go_home  # consistent navigation to base_url


def test_ui_click_triggers_backend(page, base_url, api_request_context) -> None:
    """
    Ensure that clicking "Add to cart" in the UI triggers the correct backend call.

    Args:
        page (Page): Playwright page fixture.
        base_url (str): Base URL of the application under test.
        api_request_context (APIRequestContext): Playwright API context fixture.

    Verifies:
        - POST request is sent to /add-to-cart endpoint.
        - Request body contains correct itemId.
        - Response status is 2xx or allowed 3xx redirect.

    Notes:
        This test covers only the UI → Network layer, not DB validation.
    """
    item_id = 1

    # --- Arrange: ensure a clean state ---
    reset_cart(api_request_context)

    # --- Act: navigate to homepage ---
    go_home(page, base_url)

    # Locate the specific form for the target item
    item_form = page.locator(
        f'form:has(input[name="itemId"][value="{item_id}"])'
    )
    assert item_form.first.is_visible(), (
        "Item form not visible; check selectors or seed data."
    )

    # Monitor network calls while clicking the button
    with page.expect_request("**/add-to-cart") as req_info, \
         page.expect_response("**/add-to-cart") as resp_info:
        item_form.get_by_role("button").click()

    req = req_info.value
    resp = resp_info.value

    # --- Assert: request properties ---
    assert req.method == "POST", f"Expected POST, got {req.method}"
    post_data = req.post_data or ""
    assert f"itemId={item_id}" in post_data, (
        f"Unexpected post_data: {post_data}"
    )

    # --- Assert: response status ---
    # This app uses a redirect after adding to cart, so 3xx is acceptable
    assert resp.status in (200, 302, 303), (
        f"Backend call failed: {resp.status} {resp.url}"
    )

    print(f"✅ UI click sent POST /add-to-cart with itemId={item_id} "
          f"and got {resp.status}")
