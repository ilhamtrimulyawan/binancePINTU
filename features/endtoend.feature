Feature: End-to-End Spot Trading Flow

  Scenario: Place and verify a limit buy order
    When I send a POST request to "/api/v3/order" with valid payload
    Then the response status should be 200
    And the response should contain "orderId"

    When I send GET request to "/api/v3/openOrders" with symbol "BTCUSDT"
    Then the response status should be 200
