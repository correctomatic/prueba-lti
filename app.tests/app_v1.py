from flask import Flask, request, render_template_string
import oauthlib.oauth1
from oauthlib.oauth1 import RequestValidator, SignatureOnlyEndpoint
from oauthlib.common import Request as OAuthRequest

app = Flask(__name__)

# Secret key for your tool
SECRET_KEY = 'your_secret_key'

# Sample LTI Tool Configuration
LTI_CONSUMERS = {
    'consumer_key': {
        'secret': SECRET_KEY,
        'name': 'Sample Consumer'
    }
}

class LTIRequestValidator(RequestValidator):
    def __init__(self):
        self.client_key_length = (3, 256)
        self.allowed_signature_methods = ['HMAC-SHA1']
        self.timestamp_lifetime = 60 * 5  # In seconds, five minutes

    def validate_client_key(self, client_key, request):
        return client_key in LTI_CONSUMERS

    def get_client_secret(self, client_key, request):
        return LTI_CONSUMERS[client_key]['secret']

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        return True  # This should validate the timestamp and nonce to prevent replay attacks

validator = LTIRequestValidator()
endpoint = SignatureOnlyEndpoint(validator)

@app.route('/lti_launch', methods=['POST'])
def lti_launch():
    headers, body = request.headers, request.form.to_dict()
    uri = request.url
    http_method = request.method

    # Validate the request
    oauth_request = OAuthRequest(uri, http_method, body, headers)
    valid, _ = endpoint.validate_request(oauth_request.uri, oauth_request.http_method, oauth_request.body, oauth_request.headers)
    if not valid:
        return "Invalid LTI Launch Request", 400

    # Extract parameters from the LTI Launch Request
    context_id = request.form.get('context_id')
    user_id = request.form.get('user_id')
    roles = request.form.get('roles')
    user_name = request.form.get('lis_person_name_full')
    user_email = request.form.get('lis_person_contact_email_primary')

    # Render a simple response page
    return render_template_string("""
        <h1>LTI Launch Successful</h1>
        <p>Context ID: {{ context_id }}</p>
        <p>User ID: {{ user_id }}</p>
        <p>Roles: {{ roles }}</p>
        <p>User Name: {{ user_name }}</p>
        <p>User Email: {{ user_email }}</p>
    """, context_id=context_id, user_id=user_id, roles=roles, user_name=user_name, user_email=user_email)

if __name__ == '__main__':
    app.run(debug=True)
