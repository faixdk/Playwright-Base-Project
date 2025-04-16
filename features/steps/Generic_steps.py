from behave import *
from Utils import Generic_functions


@given("I am on google home page")
def step_impl(context):
    context.page.goto("https://www.google.com")


@when("I click {locator}")
def step_impl(context, locator):
    Generic_functions.click_element(context, locator)


@step("I enter {data} in {locator} field")
def step_impl(context, data, locator):
    Generic_functions.type_data(context, locator, data)
