[![Playwright Tests](https://github.com/stuartsmith-test/e2e-playwright/actions/workflows/python-playwright.yml/badge.svg)](https://github.com/stuartsmith-test/e2e-playwright/actions/workflows/python-playwright.yml)

# E2E Automation Practice with Playwright and Python

This repository is part of a personal initiative to explore popular test automation frameworks, using AI to accelerate learning and experimentation.

Rather than showcasing deep coding expertise, the aim is to understand how modern QA practices can be enriched through AI‑assisted development. Most code structure and syntax were produced with AI support to enable rapid prototyping of real‑world end‑to‑end scenarios.

These tests are intentionally lightweight — designed for exploration, not production use. The chosen test application provides a complete UI/API/DB flow, enabling full‑stack validation without the need to build a custom SUT.<br><br>   

> **Note**  
> This test project targets my fork of the [LinkedIn Learning Test Automation Foundations app](https://github.com/stuartsmith-test/test-automation-foundations-728391), which serves as the system under test for API → DB → UI flows.

&nbsp;

**Testing flow details**  
See [`TESTING.md`](./TESTING.md) for detailed information about running and maintaining tests in this project.<br><br>

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Repo Structure](#repo-structure)
3. [How CI Runs](#how-ci-runs)
4. [Notes](#notes)
5. [License](#license)

---

## Prerequisites

Before running these Playwright + Python tests, make sure you have the necessary tools, libraries, and the sample app running.  

This alignment mirrors the setup from my AI‑assisted automation experiments, so results are consistent across local runs and pipelines.


1. **Clone and start the sample app (separate repo)**
   ```bash
   git clone https://github.com/stuartsmith-test/test-automation-foundations-728391.git
   cd test-automation-foundations-728391
   npm install
   npm start
   # App runs at http://localhost:3000

   ```

2. **Set up this test project (Python venv + deps)**  
   In a new terminal, return to the test repo and activate the virtual environment:
   ```bash
   cd ~/Projects/e2e-playwright
   python -m venv venv
   # Activate the venv
   # Git Bash:
   source venv/Scripts/activate  
   # PowerShell:
   # .\venv\Scripts\Activate.ps1

   pip install -r requirements.txt
   python -m playwright install
   ```

3. **Run a test**  
   Still in the venv:
   - UI smoke test
   ```bash
   pytest -s -v tests/ui/test_homepage.py

   ```
   - API test
   ```bash
   pytest -s -v tests/api/test_add_to_cart.py
   ```


---

## Repo Structure

A quick map of files and folders so you can navigate the project efficiently.  

The layout reflects how I organized work during AI‑assisted development — keeping fixtures, helpers, and tests cleanly separated for clarity and reuse.


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
## How CI runs

This section shows how the suite ties into automated pipelines for continuous validation, using GitHub Actions to spin up the sample app, then run Playwright/pytest against it. 

The integration pattern enables AI‑informed test automation in a CI/CD context.

**What the workflow does**
1. Checks out this repo
2. Clones my fork of the LinkedIn Learning app into `app-under-test/`
3. Starts the app on `http://localhost:3000`
4. Sets `DB_PATH` to point to the app’s `shop.db` for DB assertions
5. Runs all tests (`pytest`) against the live app

---

## Notes

Additional context, tips, and usage details collected during development. 

Many of these came from refining AI‑suggested approaches to fit the project’s scope and maintainability goals.

- This project uses `playwright` with `pytest` in a Python virtual environment.
- The system under test (SUT) is a separate Node.js app cloned from LinkedIn Learning.
- *This repo focuses on **test development only**, not app development*.
- `base_url` is set once in `pytest.ini` (used by both UI and API via fixtures).
- Run headed mode with `--headed`, or set `PWDEBUG=1` to launch Playwright Inspector for debugging.
- Future plan: integrate with QASE.io to automatically update test cases with pass/fail results after each run.

---

## License

This project is licensed under the [MIT License](LICENSE).
---