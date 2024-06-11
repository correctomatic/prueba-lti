import urllib.parse
import hmac
import hashlib
import base64
import time

# Data provided
oauth_consumer_key = 'this-is-the-consumer-key'
oauth_signature_method = 'HMAC-SHA1'
oauth_timestamp = '1718020826'
oauth_nonce = 'c25315a36c2c59ad8ca68a4b17a8b133'
oauth_callback = 'about:blank'
oauth_signature = 'T/lTuvk11WE2pm4peWwbQWbg6HA='
oauth_version = '1.0'

LTI_CONSUMER_KEY = 'this-is-the-consumer-key'
LTI_CONSUMER_SECRET = 'this-is-the-shared-secret'
http_method = 'POST'
base_url = 'https://your-lti-provider.com/launch'  # Replace with the actual base URL
base_url = 'http://localhost:5000/launch'


# Step 1: Collect the parameters
params = {
    'oauth_consumer_key': oauth_consumer_key,
    'oauth_signature_method': oauth_signature_method,
    'oauth_timestamp': oauth_timestamp,
    'oauth_nonce': oauth_nonce,
    'oauth_callback': oauth_callback,
    'oauth_version': oauth_version
}

# Step 2: Create the base string
# Normalize parameters
normalized_params = '&'.join(
    f"{urllib.parse.quote(k, safe='')}{'' if v == '' else '=' + urllib.parse.quote(v, safe='')}"
    for k, v in sorted(params.items())
)

# Create the base string
base_string = '&'.join(map(urllib.parse.quote, [http_method.upper(), base_url, normalized_params]))

# Step 3: Generate the signature
signing_key = f"{urllib.parse.quote(LTI_CONSUMER_SECRET, safe='')}&"  # Note: token_secret is empty
hashed = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1)
generated_signature = base64.b64encode(hashed.digest()).decode()

# Step 4: Compare the signatures
is_valid = urllib.parse.unquote(oauth_signature) == generated_signature

print(f"Base String: {base_string}")
print(f"Generated Signature: {generated_signature}")
print(f"Provided Signature: {urllib.parse.unquote(oauth_signature)}")
print(f"Signature Valid: {is_valid}")
