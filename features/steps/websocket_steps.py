from time import sleep
from utils.websocket_helpers import messages, connect_to_websocket

@given("I connect to the depth WebSocket stream")
def step_connect_ws(context):
    context.ws = connect_to_websocket()

@given("I connect to a WebSocket stream with invalid symbol")
def step_invalid_ws(context):
    context.ws = connect_to_websocket("invalidsymbol123")

@then("I should receive a valid depth update")
def step_validate_message(context):
    assert len(messages) > 0, "No message received"
    last = messages[-1]
    print("DEBUG LAST:", last)  # optional
    assert isinstance(last.get("b"), list), "Missing 'b' (bids) field"
    assert isinstance(last.get("a"), list), "Missing 'a' (asks) field"

@then("I should not receive a valid depth update")
def step_no_valid_message(context):
    assert len(messages) == 0 or ("bids" not in messages[-1] and "asks" not in messages[-1])

@when("I listen for a message")
def step_listen_message(context):
    max_wait = 15
    waited = 0
    while waited < max_wait:
        if messages:
            break
        sleep(1)
        waited += 1