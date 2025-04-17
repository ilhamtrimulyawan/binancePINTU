from behave import when, then
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from utils.auth import API_KEY, API_SECRET, BASE_URL


def create_signature(params, secret):
    query_string = urlencode(params)
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def send_signed_get(endpoint, params, api_key, secret):
    params["timestamp"] = int(time.time() * 1000)
    params["signature"] = create_signature(params, secret)
    headers = {"X-MBX-APIKEY": api_key}
    return requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)


def send_signed_post(endpoint, params, api_key, secret):
    params["timestamp"] = int(time.time() * 1000)
    params["signature"] = create_signature(params, secret)
    headers = {"X-MBX-APIKEY": api_key}
    return requests.post(f"{BASE_URL}{endpoint}", headers=headers, params=params)


@when('I send GET request to "{endpoint}" with symbol "{symbol}"')
def step_get_with_symbol(context, endpoint, symbol):
    context.response = send_signed_get(endpoint, {"symbol": symbol}, API_KEY, API_SECRET)
    print("🔍 Response JSON:", context.response.json())

@when('I send GET request to "{endpoint}" with valid API key')
def step_get_valid_key(context, endpoint):
    context.response = send_signed_get(endpoint, {}, API_KEY, API_SECRET)


@when('I send GET request to "{endpoint}" with invalid secret')
def step_get_invalid_secret(context, endpoint):
    context.response = send_signed_get(endpoint, {}, API_KEY, "WRONG_SECRET")


@when('I send GET request to "{endpoint}" with params "{query}"')
def step_get_with_query_string(context, endpoint, query):
    from urllib.parse import parse_qs
    raw_params = dict(item.split("=") for item in query.split("&"))
    context.response = send_signed_get(endpoint, raw_params, API_KEY, API_SECRET)

@then('the response status should be {status_code:d}')
def step_status_check(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"


@then('the response should be a list (possibly empty)')
def step_list_check(context):
    assert isinstance(context.response.json(), list)


@then('the response should contain a list of trades')
def step_trade_list(context):
    trades = context.response.json()
    assert isinstance(trades, list)


@then('the response should include balances')
def step_check_balances(context):
    data = context.response.json()
    assert "balances" in data and isinstance(data["balances"], list)

@then('the response should contain "{key}"')
def step_response_has_key(context, key):
    data = context.response.json()
    assert key in data


@then('the response should contain error message "{message}"')
def step_error_message(context, message):
    data = context.response.json()
    assert message.lower() in str(data).lower(), f"Expected error message '{message}', got {data}"

@when('I send a DELETE request to "{endpoint}" with that orderId')
def step_impl_delete_order(context, endpoint):
    order_id = context.orderId 
    params = {
        "symbol": "BTCUSDT",
        "orderId": order_id,
        "timestamp": int(time.time() * 1000)
    }
    params["signature"] = create_signature(params, API_SECRET)
    headers = {"X-MBX-APIKEY": API_KEY}
    context.response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers, params=params)

@then('the response should contain the previously created orderId')
def step_impl_verify_orderid(context):
    data = context.response.json()
    assert any(str(context.orderId) == str(order["orderId"]) for order in data), \
        f"Order ID {context.orderId} not found in response: {data}"
    print("✅ Order ID found:", context.orderId)

@then('the response should confirm order cancellation')
def step_impl_cancel_confirm(context):
    data = context.response.json()
    assert "status" in data and data["status"] == "CANCELED", f"Expected canceled status, got {data}"

@when('I send POST request to "{endpoint}" with the following body')
def step_impl_create_order(context, endpoint):
    body = json.loads(context.text)
    response = send_signed_post(endpoint, body, API_KEY, API_SECRET)
    context.response = response

    response_json = response.json()
    context.orderId = response_json["orderId"] 
    print("📌 Created Order ID:", context.orderId)
