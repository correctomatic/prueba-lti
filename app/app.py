# app.py
from flask import Flask, request, render_template_string
import logging

import oauthlib.oauth1
from oauthlib.oauth1 import RequestValidator, SignatureOnlyEndpoint

logging.basicConfig(level=logging.DEBUG)

class LTIRequestValidator(RequestValidator):
    def __init__(self, consumers):
        self.consumers = consumers

    def get_client_secret(self, client_key, request):
        return self.consumers.get(client_key)

    def validate_client_key(self, client_key, request):
        return client_key in self.consumers

    def validate_request(self, request):
        return True

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        # For simplicity, we're not checking for nonce reuse here.
        return True

consumers = {
    'your_consumer_key': 'your_consumer_secret'
}

validator = LTIRequestValidator(consumers)
endpoint = SignatureOnlyEndpoint(validator)

app = Flask(__name__)

@app.route('/launch', methods=['POST'])
def launch():
    uri, http_method, body, headers = request.url, request.method, request.form, request.headers
    valid, oauth_request = endpoint.validate_request(uri, http_method, body, headers)
    if not valid:
        return 'Unauthorized', 401

    return render_template_string('<h1>LTI Launch Successful</h1>')

@app.route('/')
def index():
    return 'Welcome to the LTI Tool'

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
