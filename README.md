[![Playwright Tests](https://github.com/stuartsmith-test/e2e-playwright/actions/workflows/python-playwright.yml/badge.svg)](https://github.com/stuartsmith-test/e2e-playwright/actions/workflows/python-playwright.yml)

# E2E Automation Practice with Playwright and Python

> **Note**  
> This test project targets my fork of the [LinkedIn Learning Test Automation Foundations app](https://github.com/stuartsmith-test/test-automation-foundations-728391), which serves as the system under test for API → DB → UI flows.

---

## Prerequisites

Before running tests, start the **sample app** this repo targets.

1. **Clone and start the app (separate repo)**
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
   # . .\venv\Scripts\Activate.ps1

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
## CI/CD

CI/CD integration (e.g., GitHub Actions) is planned but not yet implemented. Once added, this section will include setup details and test execution workflows.

## Notes

- This project uses `playwright` with `pytest` in a Python virtual environment.
- The system under test (SUT) is a separate Node.js app cloned from LinkedIn Learning.
- *This repo focuses on **test development only**, not app development*.
- `base_url` is set once in `pytest.ini` (used by both UI and API via fixtures).
- Run headed mode with `--headed`, or `PWDEBUG=1` for Inspector.

## Testing
For detailed information about running and maintaining tests in this project, see [TESTING.md](TESTING.md).

## License

This project is licensed under the [MIT License](LICENSE).