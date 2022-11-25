@first_iteration
Feature: make a drink

  Scenario Outline: selected drink is created
    Given drink_maker
    When  drink_maker is turn on
    And <drink> with <sugar_amount> is ordered
    And order is running
    Then selected <drink> is created with <sugar_amount> of sugar and stick = <is_stick>

    Examples: Drinks
      | drink     | sugar_amount | is_stick |
      | coffee    | 2            | True     |
      | tea       | 1            | True     |
      | chocolate | 0            | False    |
