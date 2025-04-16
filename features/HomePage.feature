Feature: Test page

  @test
  Scenario: testing framework
    Given I am on google home page
    When I click ACCEPT_COOKIES
    When I click SEARCH_BAR
    And I enter data in SEARCH_BAR field