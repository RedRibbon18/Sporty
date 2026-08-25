# Sporty Test Automation Framework

This workspace contains the resolution of a Sporty take home assignment, which  consists of 
   - `part_A`: manual QA: 
       - **test plan** in file `Single bet placement Test Plan.md`
       - **Test ran** and **bug report** in file `Bug report.md`
   - `part_B`: automation framework with an E2E test and an API test using `pytest`, `selenium`, and `requests`.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run tests

- Run all tests:
  ```bash
  pytest part_B
  ```

- Run only E2E tests:
  ```bash
  pytest part_B/tests/e2e
  ```

- Run only API tests:
  ```bash
  pytest part_B/tests/api
  ```

- Use environment configuration for tests:
  ```bash
  pytest part_B/tests/e2e --env qa
  pytest part_B/tests/api --env prod
  ```

- Run smoke tests only:
  ```bash
  cd part_B
  pytest -m smoke --user-id candidate-J8g8HD3Lsw
  ```

- Run regression tests only:
  ```bash
  cd part_B
  pytest -m regression --user-id candidate-J8g8HD3Lsw
  ```

- Use a custom base URL for E2E tests:
  ```bash
  pytest part_B/tests/e2e --browser firefox --headless --base-url https://your-app.example.com  --user-id candidate-J8g8HD3Lsw
  ```

- Set environment in shell via `TEST_ENV`:
  ```bash
  cd part_B
  $env:TEST_ENV = "qa"
  pytest part_B/tests/e2e --user-id candidate-J8g8HD3Lsw
  ```

## Structure

- `framework/drivers`: WebDriver setup
- `framework/pages`: Page objects for E2E tests
- `framework/components`: Component objects for E2E, such as modals, toolbars, etc
- `framework/api`: Reusable API client code
- `tests/e2e`: End-to-end test cases
- `tests/api`: API test cases
