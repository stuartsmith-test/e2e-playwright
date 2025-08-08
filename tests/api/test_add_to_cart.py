import pytest
from playwright.sync_api import APIRequestContext

# Base URL of the test app (make sure the app is running locally)
BASE_URL = "http://localhost:3000"

# This fixture creates a reusable API client for all tests in this session
# It uses the Playwright APIRequestContext to make HTTP requests.
@pytest.fixture(scope="session")
def api_request_context(playwright):
    # Create a new API request context with the base URL
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context  # This makes it available to the test function
    request_context.dispose()  # Clean up after tests are done


def test_add_to_cart(api_request_context: APIRequestContext):
    """
    This test does the following:
    1. Sends a POST request to /add-to-cart with a valid itemId
    2. Asserts that the response status code is 200
    """

    # Step 1: Reset the cart
    reset_response = api_request_context.post("/reset-cart")
    assert reset_response.ok, f"Cart reset failed: {reset_response.status}"

    # Step 2: Prepare the payload with a valid item ID from the database
    payload = {"itemId": 1}  # Assume item with ID 1 exists

    # Step 3: Send the POST request to /add-to-cart
    response = api_request_context.post("/add-to-cart", data=payload)

    # Step 4: Assert that the response status is 2xx
    assert response.ok, f"Unexpected status: {response.status}"

    # Optional: Print for debug purposes
    print(f"✅ Cart was reset and item {payload['itemId']} was successfully added.")
