Feature: Binance WebSocket Depth Stream

  Scenario: Connect to Binance depth WebSocket and receive order book updates
    Given I connect to the depth WebSocket stream
    When I listen for a message
    Then I should receive a valid depth update

  Scenario: Connect with invalid symbol to get error
    Given I connect to a WebSocket stream with invalid symbol
    When I listen for a message
    Then I should not receive a valid depth update
