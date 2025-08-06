# E2E Automation Practice with Playwright and Python

> **Note**  
> This test project targets my fork of the [LinkedIn Learning Test Automation Foundations app](https://github.com/stuartsmith-test/test-automation-foundations-728391), which serves as the system under test for API → DB → UI flows.

---

## Prerequisites

Before running any tests, you’ll need to clone and start the test app that this project targets.

1. **Clone and start the test app**  
   ```bash
   git clone https://github.com/stuartsmith-test/test-automation-foundations-728391.git
   cd test-automation-foundations-728391
   npm install
   npm start
   ```

2. **Initialize the SQLite database**  
   In a new terminal, return to the test repo and activate the virtual environment:
   ```bash
   cd ~/Projects/e2e-playwright
   source venv/Scripts/activate   # Windows Git Bash
   python init_db.py
   ```

3. **Run a test**  
   Still in the venv:
   ```bash
   pytest tests/api/test_users.py -v
   ```

---

## Repo Structure

```text
e2e-playwright/
├── data/                  # Contains the SQLite database (gitignored)
├── tests/                 # API, UI, and E2E tests
├── utils/                 # Helper modules (e.g., db access)
├── init_db.py             # Script to seed database
├── requirements.txt
└── README.md
```

---

## Notes

- This project uses `playwright` with `pytest` in a Python virtual environment.
- The system under test (SUT) is a separate Node.js app cloned from LinkedIn Learning.
- This repo focuses on **test development only**, not app development.
