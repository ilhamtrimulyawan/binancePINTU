from behave import when, then
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from utils.auth import API_KEY, API_SECRET, BASE_URL

def create_signature(params):
    query_string = urlencode(params)
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

@when('I send a POST request to "{endpoint}" with valid payload')
def step_valid_order(context,endpoint):
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "price": "25000",
        "quantity": "0.001",
        "timeInForce": "GTC",
        "timestamp": timestamp
    }
    params["signature"] = create_signature(params)
    headers = {"X-MBX-APIKEY": API_KEY}
    context.response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, params=params)

@when('I send a POST request to "/api/v3/order" with missing quantity')
def step_missing_quantity(context):
    endpoint = "/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "price": "25000",
        "timeInForce": "GTC",
        "timestamp": timestamp
    }
    params["signature"] = create_signature(params)
    headers = {"X-MBX-APIKEY": API_KEY}
    context.response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, params=params)

@when('I send a POST request to "/api/v3/order" with invalid API key')
def step_invalid_key(context):
    endpoint = "/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "price": "25000",
        "quantity": "0.001",
        "timeInForce": "GTC",
        "timestamp": timestamp
    }
    params["signature"] = create_signature(params)
    headers = {"X-MBX-APIKEY": "INVALID_API_KEY"}
    context.response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, params=params)
