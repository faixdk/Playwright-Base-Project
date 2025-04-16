from locators import Generic_locators
import time

def click_element(context, locator):
    element = get_element(context, locator)
    element.click()

def type_data(context, locator, data):
    element = get_element(context, locator)
    element.fill(data)

def get_element(context, locator):
    selector = Generic_locators.Locators[locator][0]
    element = context.page.locator(selector)
    wait_for_element(element)
    return element


def wait_for_page_load(context, timeout=30000):
    context.page.wait_for_load_state('networkidle', timeout=timeout)

def wait_for_element(element, timeout=10000, state='visible'):
    element.wait_for(state=state, timeout=timeout)

def get_text(context, locator):
    element = get_element(context, locator)
    return element.text_content()

def is_element_visible(context, locator):
    element = get_element(context, locator)
    return element.is_visible()

def wait_and_click(context, locator):
    element = get_element(context, locator)
    element.click()
    time.sleep(0.5)

def navigate_to(context, url):
    """Navigate to a URL and wait for the page to load"""
    context.page.goto(url)
    wait_for_page_load(context)

def expect_element(context, locator, condition='visible', timeout=10000):
    from playwright.sync_api import expect
    element = get_element(context, locator)

    if condition == 'visible':
        expect(element).to_be_visible(timeout=timeout)
    elif condition == 'hidden':
        expect(element).to_be_hidden(timeout=timeout)
    elif condition == 'enabled':
        expect(element).to_be_enabled(timeout=timeout)
    elif condition == 'disabled':
        expect(element).to_be_disabled(timeout=timeout)
    return True