from playwright.sync_api import sync_playwright
import os
import shutil

def clean_reports_folder():
    """Clean up old reports before starting new tests"""
    # Clean videos directory
    if os.path.exists('reports/videos'):
        shutil.rmtree('reports/videos')

    # Clean screenshots directory
    if os.path.exists('allure-results'):
        shutil.rmtree('allure-results')

        # Clean allure directory
    if os.path.exists('reports/screenshots'):
        shutil.rmtree('reports/screenshots')

    # Recreate directories
    os.makedirs('reports/videos', exist_ok=True)
    os.makedirs('reports/screenshots', exist_ok=True)
    print("Reports folder cleaned")

def get_browser():
    """Initialize and return browser components"""
    # Clean reports folder
    clean_reports_folder()

    # Start Playwright
    playwright = sync_playwright().start()

    # Launch browser
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
    )

    # Set up context with recording
    browser_context = browser.new_context(
        record_video_dir='reports/videos',
        record_video_size={"width": 1920, "height": 1080},
        no_viewport=True  # Remove viewport constraints for maximization
    )

    # Set timeouts
    browser_context.set_default_timeout(30000)

    # Create page
    page = browser_context.new_page()

    # Maximize window using JavaScript
    # page.evaluate("""() => {
    #     window.moveTo(0, 0);
    #     window.resizeTo(screen.availWidth, screen.availHeight);
    # }""")

    # Return all components
    return (page, browser_context, browser, playwright)