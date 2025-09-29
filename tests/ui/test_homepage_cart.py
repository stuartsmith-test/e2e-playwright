"""Homepage cart interaction tests: add-to-cart messaging, cart count, and max quantity state.

These UI tests sometimes need to manipulate server state (e.g., reset the cart) to
start from a clean baseline. Playwright exposes HTTP capabilities via an
`APIRequestContext` type, which we can obtain in two common ways:

- In API-focused tests, we receive an `api_request_context` fixture directly and pass
  it to helpers like `reset_cart(api_request_context)`.
- In UI-focused tests, we don't have that fixture, but each `Page` exposes an
  `APIRequestContext` at `page.request`. We can pass that into the same helpers, e.g.,
  `reset_cart(page.request)`. Both satisfy the same interface and behave equivalently.

Using the shared helper keeps assertions (e.g., expecting OK status) and endpoint
paths centralized in `utils/api_helpers.py`, so we don’t duplicate those details in
every test.
"""

from playwright.sync_api import Page, expect
from utils.ui_helpers import go_home, expect_text_visible, get_cart_count
from utils.api_helpers import reset_cart


def test_add_to_cart_shows_message_and_updates_cart_count(page: Page, base_url: str) -> None:
    """After adding an item, success notification appears and cart count increments by 1."""
    # Arrange: reset cart to a known state and open home
    reset_cart(page.request)
    go_home(page, base_url)

    initial_count = get_cart_count(page)

    # Act: add the first item (form submit triggers a redirect to /?message=...)
    with page.expect_navigation():
        page.click("#add-to-cart-1")

    # Assert: success message and incremented count
    expect_text_visible(page, "Item successfully added to cart")
    expect(page.locator("#cart-link span")).to_have_text(str(initial_count + 1))


def test_add_button_disables_at_max_quantity(page: Page, base_url: str) -> None:
    """Button disables and max-quantity message appears after reaching quantity 10."""
    # Arrange: reset and open home
    reset_cart(page.request)
    go_home(page, base_url)

    add_btn = page.locator("#add-to-cart-1")

    # Act: click until the item reaches the maximum (10); each submit redirects
    for _ in range(10):
        with page.expect_navigation():
            add_btn.click()

    # Assert: button disabled and max message visible
    expect(add_btn).to_be_disabled()
    expect(page.get_by_text("Maximum quantity reached").first).to_be_visible()


