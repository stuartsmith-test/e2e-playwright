# utils/ui_helpers.py
from playwright.sync_api import Page

def go_home(page: Page, base_url: str) -> None:
    """Navigate to the home page and wait for initial DOM readiness."""
    page.goto(base_url + "/")
    page.wait_for_load_state("domcontentloaded")

def expect_text_visible(page: Page, text: str) -> None:
    """Assert that the given text is visible on the page."""
    assert page.get_by_text(text).first.is_visible(), f"'{text}' not visible on page"

