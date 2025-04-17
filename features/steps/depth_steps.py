from behave import when, then
import requests
from utils.auth import BASE_URL


@then('the response should contain bids and asks')
def step_impl(context):
    data = context.response.json()
    assert "bids" in data and isinstance(data["bids"], list)
    assert "asks" in data and isinstance(data["asks"], list)
