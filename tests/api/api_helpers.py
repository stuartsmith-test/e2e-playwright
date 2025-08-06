from playwright.sync_api import APIRequestContext, Playwright

BASE_URL = "http://localhost:3000/api"  # <-- replace with sample app API URL

def create_api_context(playwright: Playwright) -> APIRequestContext:
    """
    Create and return a Playwright APIRequestContext for making API calls.
    """
    return playwright.request.new_context(base_url=BASE_URL)

def create_user_api(api_context: APIRequestContext, username: str, email: str, password: str):
    """
    Create a new user via API and return the response JSON.
    """
    response = api_context.post("/users", data={
        "username": username,
        "email": email,
        "password": password
    })
    assert response.ok, f"Failed to create user: {response.status} {response.text()}"
    return response.json()

def get_user_api(api_context: APIRequestContext, user_id: int):
    """
    Get user details by ID via API and return JSON.
    """
    response = api_context.get(f"/users/{user_id}")
    assert response.ok, f"Failed to fetch user: {response.status} {response.text()}"
    return response.json()

def delete_user_api(api_context: APIRequestContext, user_id: int):
    """
    Delete user by ID via API.
    """
    response = api_context.delete(f"/users/{user_id}")
    assert response.ok, f"Failed to delete user: {response.status} {response.text()}"
