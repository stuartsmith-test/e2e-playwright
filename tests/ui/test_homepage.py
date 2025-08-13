# tests/ui/test_homepage.py
"""UI smoke test: home page loads and shows a known seeded item ('Koala')."""

from playwright.sync_api import Page  # Playwright page object type for clarity in IDEs
from utils.ui_helpers import go_home, expect_text_visible  # shared nav + visibility helpers


def test_homepage_loads_and_shows_items(page: Page, base_url: str) -> None:
    """Load home page and assert a seeded catalog item is visible."""
    # Arrange/Act: open home
    go_home(page, base_url)

    # Assert: we're on the base URL, and the seeded item appears
    page.wait_for_url(base_url)
    expect_text_visible(page, "Koala")

    print("✅ Homepage loaded; 'Koala' is visible.")
