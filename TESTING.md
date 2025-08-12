# TESTING.md

## Overview
This document explains how to run and maintain tests for this project.  
It covers file structure, fixtures, helpers, and useful commands for API and UI testing.

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [How Test Discovery Works](#how-test-discovery-works)
3. [Fixtures](#fixtures)
4. [Helpers](#helpers)
5. [Running Tests](#running-tests)
6. [Headless vs. Headed Mode](#headless-vs-headed-mode)
7. [Common Gotchas](#common-gotchas)

---

## Project Structure
```text
e2e-playwright/
├── conftest.py # Shared fixtures (e.g., api_request_context)
├── pytest.ini # Pytest configuration (e.g., base_url)
├── utils/ # Reusable helper functions
│ ├── api_helpers.py # API helper functions
│ ├── dbHelpers.py # Database helper functions
│ └── ui_helpers.py # UI helper functions
├── tests/
│ ├── api/
│ │ ├── init.py
│ │ └── test_add_to_cart.py # Example API test
│ ├── db/
│ │ ├── init.py
│ │ └── test_db_connection.py # Database connection test
│ └── ui/
│ ├── init.py
│ └── test_homepage.py # Example UI test
└── requirements.txt
```

---

## How Test Discovery Works
Pytest automatically finds tests by:
- **Filename**: Any file named `test_*.py` or `*_test.py`
- **Function name**: Any function starting with `test_`
- **Class name**: Any class starting with `Test` (and containing test methods)

⚡ **Note:** Helper functions do not start with `test_` so they aren’t treated as tests.

---

## Fixtures
Fixtures provide reusable, pre-configured objects for tests.  

**Example: `api_request_context` in `conftest.py`**
```python
# conftest.py
import pytest
from typing import Generator
from playwright.sync_api import APIRequestContext, Playwright

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """
    Session-scoped API client for HTTP requests to the app.
    Uses pytest-base-url's `base_url` so API & UI agree on the host.
    """
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
```
- **Scope**: `session` → created once per test run, reused across tests.
- **Location**: In `conftest.py` so pytest auto-loads it for all tests without an import.
- **Usage**: Simply declare `api_request_context` as a parameter in a test function.

## Helpers

Helper modules live in `utils/` and contain reusable logic that keeps test files clean.

- `api_helpers.py`: API-related functions (e.g., reset_cart, add_item)

- `dbHelpers.py`: Database access and query helpers

- `ui_helpers.py`: UI functions (e.g., go_home, login_user)

Example: `reset_cart` in `api_helpers.py`

```python
# utils/api_helpers.py
from playwright.sync_api import APIRequestContext

def reset_cart(api_request_context: APIRequestContext) -> None:
    """Clear the cart via POST /reset-cart."""
    response = api_request_context.post("/reset-cart")
    assert response.ok, f"Reset cart failed. Status: {response.status}"
```
## Running Tests
Run all tests:
```bash
pytest
```

Run only API tests:
```bash
pytest tests/api
```
Run a single test file:
```bash
pytest tests/api/test_add_to_cart.py
```
Run a single test function:
```bash
pytest tests/api/test_add_to_cart.py::test_add_to_cart
```

## Headless vs. Headed Mode
Playwright runs headless (no browser window) by default.

**Run headed mode:**
```bash
pytest --headed
```
**Run headed mode for a specific browser:**
```bash
pytest --browser chromium --headed
```

## Common Gotchas
- **Fixture scope** matters — if you expect fresh state, use `function` scope instead of `session`.

- **Order of imports**: `conftest.py` is auto-loaded, so no need to import fixtures directly.

- **BASE_URL**: Comes from `pytest.ini` (via `pytest-base-url`) or `.env` for API contexts.

- **Database connections**: Always close them in helpers to avoid locks.

- **Browser cleanup**: pytest-playwright auto-closes browser contexts after each test.

