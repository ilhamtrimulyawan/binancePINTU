Feature: Account-related endpoints

  Scenario: Get open orders for active symbol
    When I send GET request to "/api/v3/openOrders" with symbol "BTCUSDT"
    Then the response status should be 200
    And the response should be a list (possibly empty)

  Scenario: Get open orders with invalid symbol
    When I send GET request to "/api/v3/openOrders" with symbol "FAKESYMBOL"
    Then the response status should be 400
    And the response should contain error message "Invalid symbol"

  Scenario: Fetch trade history
    When I send GET request to "/api/v3/myTrades" with symbol "BTCUSDT"
    Then the response status should be 200
    And the response should contain a list of trades

  Scenario: Fetch account balance
    When I send GET request to "/api/v3/account" with valid API key
    Then the response status should be 200
    And the response should include balances

  Scenario: Fetch account balance with wrong secret
    When I send GET request to "/api/v3/account" with invalid secret
    Then the response status should be 400
