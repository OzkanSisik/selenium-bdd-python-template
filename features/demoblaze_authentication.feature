Feature: DemoBlaze User Authentication
  As a user
  I want to log in to DemoBlaze
  So that I can access personalized features

  Background:
    Given I am on the DemoBlaze homepage

  Scenario: Login with valid credentials
    When I click on the "Log in" link
    And I enter username "testuser"
    And I enter password "testpass"
    And I click the "Log in" button
    Then I should see "Welcome testuser" message