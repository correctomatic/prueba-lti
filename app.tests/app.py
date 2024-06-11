from flask import Flask, request as flask_request, render_template_string
from oauthlib.oauth1 import RequestValidator, SignatureOnlyEndpoint
from oauthlib.common import Request

app = Flask(__name__)

# Your LTI credentials
LTI_CONSUMER_KEY = 'this-is-the-consumer-key'
LTI_CONSUMER_SECRET = 'this-is-the-shared-secret'

# Simple in-memory store for consumer keys and secrets
lti_credentials = {LTI_CONSUMER_KEY: LTI_CONSUMER_SECRET}

class LTIRequestValidator(RequestValidator):
    def validate_client_key(self, client_key, request):
        return client_key in lti_credentials

    def get_client_secret(self, client_key, request):
        return lti_credentials[client_key]

    def validate_request_token(self, request_token, request):
        return True

    def validate_access_token(self, client_key, token, request):
        return True

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        return True

validator = LTIRequestValidator()
endpoint = SignatureOnlyEndpoint(validator)

@app.route('/launch', methods=['POST'])
def lti_launch():
    # Convert the Flask request to an OAuthlib request
    oauth_request = Request(flask_request.url, http_method=flask_request.method, body=flask_request.form, headers=dict(flask_request.headers))

    # Validate the LTI request
    valid, _ = endpoint.validate_request(oauth_request.uri, oauth_request.http_method, oauth_request.body, oauth_request.headers)

    if not valid:
        return "Invalid LTI request", 400

    # Extract LTI parameters
    lti_params = flask_request.form.to_dict()

    # Respond to the LTI launch
    return render_template_string("""
    <h1>LTI Launch Successful</h1>
    <p>Welcome {{ lti_params['user_id'] }}!</p>
    <p>This LTI launch was made by {{ lti_params['tool_consumer_instance_name'] }}.</p>
    """, lti_params=lti_params)

if __name__ == '__main__':
    app.run(debug=True)
