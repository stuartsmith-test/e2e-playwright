# tests/ui/test_homepage.py


from utils.ui_helpers import go_home, expect_text_visible


"""
UI smoke test:
- Load the home page
- Verify a known seeded item ("Koala") is visible
"""

def test_homepage_loads_and_shows_items(page, base_url):
    go_home(page, base_url)
    assert page.title() is not None
    expect_text_visible(page, "Koala")
    print("✅ Homepage loaded and 'Koala' is visible.")
