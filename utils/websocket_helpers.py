import websocket
import json
import threading

messages = []

def on_message(ws, message):
    print("RECEIVED:", message) 
    data = json.loads(message)
    messages.append(data)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def connect_to_websocket(symbol="btcusdt"):
    url = f"wss://testnet.binance.vision/ws/{symbol}@depth"
    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
    return ws
