import pytest
from playwright.sync_api import sync_playwright, expect

def test_login_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True to hide browser
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        browser.close()