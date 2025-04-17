import hmac
import hashlib
import time
from urllib.parse import urlencode
import requests
from config.config import API_KEY, API_SECRET, BASE_URL

def create_signature(params: dict) -> str:
    query_string = urlencode(params)
    return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def signed_request(method: str, endpoint: str, params: dict = None) -> requests.Response:
    if params is None:
        params = {}
    params['timestamp'] = int(time.time() * 1000)
    params['recvWindow'] = 5000
    signature = create_signature(params)
    params['signature'] = signature
    headers = {"X-MBX-APIKEY": API_KEY}
    return requests.request(method, f"{BASE_URL}{endpoint}", headers=headers, params=params)
