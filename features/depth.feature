Feature: Order Book Depth Endpoint

  Scenario: Fetch order book with valid symbol
    When I send GET request to "/api/v3/depth" with params "symbol=BTCUSDT&limit=5"
    Then the response status should be 200
    And the response should contain bids and asks

  Scenario: Fetch order book with invalid symbol
    When I send GET request to "/api/v3/depth" with params "symbol=INVALIDPAIR&limit=5"
    Then the response status should be 400
    And the response should contain error message "Invalid symbol"
