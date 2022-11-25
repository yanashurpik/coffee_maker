@first_iteration
Feature: make a drink

  Scenario Outline: selected drink is created
    Given drink_maker
    When  drink_maker is turn on
    And <drink> is selected
    And order is running
    Then selected <drink> is created

    Examples: Drinks
      | drink     |
      | coffee    |
      | tea       |
      | chocolate |
