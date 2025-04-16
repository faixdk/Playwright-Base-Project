# Playwright Behave Framework

A streamlined, modular test automation framework using Python, Playwright, and Behave with automatic screenshot and video capture for failed tests.

## Features

- BDD approach with Behave
- Cross-browser testing with Playwright
- Automatic screenshots on test failure
- Video recording for failed tests only
- Maximized browser window
- Clean reporting structure
- Reusable utility functions
- Simple, maintainable codebase
- Allure reporting integration
- Automatic video attachment to Allure reports

## Directory Structure

```
playwright-behave-framework/
├── features/               # Behave feature files
│   └── HomePage.feature    # Example feature file
├── Utils/                  # Utility modules
│   ├── browser_helper.py   # Browser initialization
│   ├── media_utils.py      # Screenshot/video utilities
│   └── Generic_functions.py # UI interaction methods
├── locators/               # Element locators
│   └── Generic_locators.py # Element selectors
├── Generic_steps.py        # Common step definitions
├── reports/                # Test artifacts
│   ├── screenshots/        # Screenshots from failed tests
│   └── videos/             # Videos from failed tests
├── allure-results/         # Allure test results
├── allure-report/          # Generated Allure reports
├── environment.py          # Behave hooks for setup/teardown
└── behave.ini              # Behave configuration
```

## Setup

1. Install dependencies:
   ```bash
   pip install playwright behave allure-behave
   playwright install
   ```

2. Install Allure command-line tool (varies by operating system):
   ```bash
   # For Windows (using Scoop)
   scoop install allure

   # For macOS
   brew install allure

   # For Linux
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```

3. Run the tests:
   ```bash
   python -m behave
   ```

4. Generate and view Allure report:
   ```bash
   # Generate and open the Allure report
   allure generate allure-results -o allure-report --clean && allure open allure-report
   ```

## Writing Tests

### Feature Files

Create feature files in the `features` directory using Gherkin syntax:

```gherkin
Feature: Test page

  Scenario: testing framework
    Given I am on google home page
    When I click ACCEPT_COOKIES
    When I click SEARCH_BAR
    And I enter data in SEARCH_BAR field
```

### Step Definitions

Use the common steps in `Generic_steps.py` or create your own:

```python
@given("I am on google home page")
def step_impl(context):
    context.page.goto("https://www.google.com")

@when("I click {locator}")
def step_impl(context, locator):
    Generic_functions.click_element(context, locator)
```

### Locators

Define element locators in `locators/Generic_locators.py`:

```python
Locators = {
    "ACCEPT_COOKIES": ["text='Accept all'"],
    "SEARCH_BAR": ["[name='q']"]
}
```

## Key Components

### browser_helper.py

Handles browser initialization with:
- Browser launch configuration
- Window maximization
- Video recording setup
- Report folder cleanup

### media_utils.py

Manages test artifacts:
- Screenshot capture and naming
- Video processing and renaming
- File path standardization
- Attaching videos to Allure reports

### Generic_functions.py

Provides reusable UI interaction methods:
- Element clicking and typing
- Waiting for elements and page loads
- Element verification

### environment.py

Controls the test lifecycle:
- Browser setup and teardown
- Screenshot capture on failure
- Video processing
- Resource cleanup

## Video Recording

- Videos are automatically recorded for all test runs
- Only videos of failed tests are kept and renamed
- Videos follow a consistent naming pattern: feature_name_scenario_name.webm
- Videos are automatically attached to Allure reports for easy viewing
- Pages are automatically closed before video saving to comply with Playwright requirements

## Best Practices

1. **Keep locators centralized** in Generic_locators.py
2. **Use explicit waits** for reliable tests
3. **Reuse step definitions** when possible
4. **Maintain clean feature files** with focused scenarios
5. **Run tests regularly** to catch regressions early

## Troubleshooting

- If tests fail with timeout errors, adjust timeouts in Generic_functions.py
- If screenshots or videos are missing, check report folder permissions
- For browser startup issues, run `playwright install` to update browsers
- If Allure reports are empty, ensure you've installed allure-behave correctly
