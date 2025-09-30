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
7. [Continuous Integration (CI)](#continuous-integration-ci)
8. [Common Gotchas](#common-gotchas)

---

## Project Structure
```text
e2e-playwright/
├── .github/
│   └── workflows/
│       └── python-playwright.yml        # CI: spins up app-under-test and runs pytest
├── LICENSE                              # MIT License
├── README.md                            # Project overview + setup + CI badge
├── TESTING.md                           # Test structure, how to run locally/CI
├── conftest.py                          # Shared fixtures (e.g., api_request_context)
├── pytest.ini                           # pytest config (pythonpath, base_url)
├── requirements.txt                     # Top-level deps for tests
├── utils/                               # Reusable helpers (shared across tests)
│   ├── __init__.py
│   ├── api_helpers.py                   # reset_cart(), add_to_cart(), etc.
│   ├── dbHelpers.py                     # SQLite helpers (get_cart_quantity, etc.)
│   └── ui_helpers.py                    # go_home(), expect_text_visible(), etc.
└── tests/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── test_add_to_cart.py          # API-only smoke (uses Playwright API client)
    ├── db/
    │   ├── __init__.py
    │   └── test_db_connection.py        # Sanity connection/read test against shop.db
    ├── e2e/
    │   ├── __init__.py
    │   ├── test_cart_db_validation.py   # API → DB: quantity reflects API actions
    │   └── test_cart_end_to_end.py      # API → DB → UI: /cart shows correct qty
    └── ui/
        ├── __init__.py
        ├── test_homepage.py             # UI smoke: “Koala” visible on home
        └── test_add_to_cart_network.py  # UI+network: click triggers POST /add-to-cart

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

---

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
---

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
---
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
**Debug with Playwright Inspector:**
```bash
PWDEBUG=1 pytest
```
---
## Continuous Integration (CI)

This repo uses **GitHub Actions** to spin up the app-under-test and run all tests (API, DB, UI) with Playwright/pytest.

**What the workflow does**
1. Checks out this repo
2. Clones my fork of the LinkedIn Learning app into `app-under-test/`
3. Starts the app on `http://localhost:3000`
4. Sets `DB_PATH` to point to the app’s `shop.db` for DB assertions
5. Runs all tests (`pytest`) against the live app

**View current build status:** See the [CI badge in README](README.md) for the latest run result.

> **Note:** In CI (and by default in Codespaces), the sample app is cloned into an
> `app-under-test/` folder **inside this repo**. Advanced users can clone it as a
> sibling under `/workspaces/` in Codespaces, but that isn’t required.  
> The `app-under-test/` folder is ignored by `.gitignore` to avoid accidental commits.

**Manual run**
- GitHub → **Actions** → *Playwright Tests* → **Run workflow**.

**Interpreting failures**
- If “Wait for app” fails, the app didn’t start in time (increase wait loop or inspect app logs).
- If tests fail, download the **artifacts** from the run for details.  
  (Optional: enable `--tracing=retain-on-failure` and `--screenshot=only-on-failure` later.)

**Key envs (set by workflow)**
- `BASE_URL` / `PYTEST_BASE_URL`: `http://localhost:3000`
- `DB_PATH`: `${{ github.workspace }}/app-under-test/shop.db`

## Qase Integration

This project is integrated with [Qase TestOps](https://qase.io) to record automated test results.

- Each GitHub Actions run automatically creates a test run in Qase.
- Test cases are auto-created on the first run and updated with pass/fail status on later runs.
- Results are grouped under the project’s suites (`api`, `db`, `ui`, `e2e`) to match the repo structure.

### Example

Below is a screenshot of a Qase run summary created from CI:

<img src="docs/qase_run_example.png" alt="Qase Run Example" width="800">

In a real project, Qase provides full details for each run (test titles, execution history, assignments, etc.). 
This screenshot is included here only to illustrate how results are published — no Qase setup is required 
to explore the tests in this repo.

---

## Common Gotchas
- **Fixture scope** matters — if you expect fresh state, use `function` scope instead of `session`.

- **Order of imports**: `conftest.py` is auto-loaded, so no need to import fixtures directly.

- **BASE_URL**: Comes from `pytest.ini` (via `pytest-base-url`) or `.env` for API contexts.

- **Database connections**: Always close them in helpers to avoid locks.

- **Browser cleanup**: pytest-playwright auto-closes browser contexts after each test.
---
