from flask import Flask, request, render_template_string
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskRequest
import json

app = Flask(__name__)

# LTI 1.3 configuration
config = {
    "issuer": "https://platform.example.com",
    "client_id": "your_client_id",
    "auth_server": "https://platform.example.com/auth/token",
    "keyset_url": "https://platform.example.com/keys"
}

# Initialize FlaskOIDCLogin
lti = FlaskOIDCLogin(app, request_validator=None, config=config)

@app.route('/lti_launch', methods=['POST'])
@lti.validate()
def lti_launch():
    lti_launch_data = FlaskRequest(request).to_dict()

    # Extract LTI launch parameters
    context_id = lti_launch_data.get('context_id')
    user_id = lti_launch_data.get('user_id')
    roles = lti_launch_data.get('roles')
    user_name = lti_launch_data.get('lis_person_name_full')
    user_email = lti_launch_data.get('lis_person_contact_email_primary')

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
