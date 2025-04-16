from Utils.browser_helper import get_browser
from Utils.media_utils import take_screenshot, process_videos, ensure_report_folders
import time

def before_all(context):
    # Ensure report folders exist
    ensure_report_folders()

    # Get all the browser components
    page, browser_context, browser, playwright = get_browser()

    # Store everything in the behave context
    context.page = page
    context.browser_context = browser_context
    context.browser = browser
    context.playwright = playwright

    # Store current feature and scenario names
    context.current_feature = None
    context.current_scenario = None

    # Store failed scenarios to track which videos to keep
    context.failed_scenarios = []

def before_feature(context, feature):
    # Store current feature name
    context.current_feature = feature.name

def before_scenario(context, scenario):
    # Store current scenario name
    context.current_scenario = scenario.name

def after_scenario(context, scenario):
    # Handle failed scenarios
    if scenario.status == "failed":
        # Add to failed scenarios list
        if not hasattr(context, 'failed_scenarios'):
            context.failed_scenarios = []

        # Record failure info
        context.failed_scenarios.append({
            'feature': context.current_feature,
            'scenario': context.current_scenario
        })

        # Take screenshot on failure
        if hasattr(context, 'page'):
            take_screenshot(context.page, context.current_feature, context.current_scenario)

    # Add a brief wait after each scenario to allow operations to complete
    try:
        if hasattr(context, 'page'):
            context.page.wait_for_load_state('networkidle')
    except Exception as e:
        print(f"Wait error: {str(e)}")

    # First close browser
    if hasattr(context, 'page') and context.page:
        try:
            context.page.wait_for_load_state('networkidle')
        except:
            pass
        context.page.close()

    if hasattr(context, 'browser_context') and context.browser_context:
        context.browser_context.close()

    # Then process videos after the page is closed
    if scenario.status == "failed" and hasattr(context, 'failed_scenarios'):
        process_videos(context, context.failed_scenarios)


def after_feature(context, feature):
    # Wait before closing the page to ensure everything completes
    try:
        if hasattr(context, 'page') and context.page:
            # Wait for network to be idle before closing
            context.page.wait_for_load_state('networkidle')
            # Close remaining resources
        if hasattr(context, 'browser') and context.browser:
            context.browser.close()

        if hasattr(context, 'playwright') and context.playwright:
            context.playwright.stop()
    except Exception as e:
        print(f"Wait error in after_feature: {str(e)}")

# def after_all(context):
#     # Add a delay to ensure everything finishes
#     time.sleep(2)



