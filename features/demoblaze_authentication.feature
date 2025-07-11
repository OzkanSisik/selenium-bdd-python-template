Feature: DemoBlaze User Authentication
  As a user
  I want to log in to DemoBlaze
  So that I can access personalized features

  Background:
    Given I am on the DemoBlaze homepage

  Scenario: Login with valid credentials
    When I click on the "Log in" link
    And I enter username "ozkanuser"
    And I enter password "ozkanpass"
    And I click the "Log in" button
    Then I should see "Welcome ozkanuser" message
    