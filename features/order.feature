Feature: Order endpoint

  Scenario: Place a valid limit buy order
    When I send a POST request to "/api/v3/order" with valid payload
    Then the response status should be 200
    And the response should contain "orderId"

  Scenario: Place order with missing quantity
    When I send a POST request to "/api/v3/order" with missing quantity
    Then the response status should be 400
    And the response should contain error message "Mandatory parameter 'quantity' was not sent"

  Scenario: Place order with invalid API key
    When I send a POST request to "/api/v3/order" with invalid API key
    Then the response status should be 401
    And the response should contain error message "api-key format invalid."
