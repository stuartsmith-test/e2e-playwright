# utils/ui_helpers.py
"""UI helpers for common navigation and assertions in Playwright tests."""

from playwright.sync_api import Page  # Playwright page object used by tests

def go_home(page: Page, base_url: str) -> None:
    """Navigate to the app homepage and wait for DOM readiness.

    This relies on Playwright's built-in auto-waiting. We avoid explicit timeouts
    unless we encounter slow environments (e.g., CI) where defaults are insufficient.
    """
    page.goto(base_url)
    page.wait_for_url(base_url)
    page.wait_for_load_state("domcontentloaded")


def expect_text_visible(page: Page, text: str) -> None:
    """Assert that the given text is visible somewhere on the page."""
    assert page.get_by_text(text).first.is_visible(), f"'{text}' not visible on page"
