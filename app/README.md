Launch app:

python 


Example LTI Launch Request
Here's an example of the data included in an LTI launch request:

plaintext
Copiar código
POST /lti_launch HTTP/1.1
Host: toolprovider.example.com
Content-Type: application/x-www-form-urlencoded

lti_message_type=basic-lti-launch-request
lti_version=LTI-1p0
resource_link_id=unique-link-id
user_id=unique-user-id
roles=Learner
oauth_consumer_key=consumer-key
oauth_signature_method=HMAC-SHA1
oauth_timestamp=137131200
oauth_nonce=abcdef123456
oauth_version=1.0
oauth_signature=generated-oauth-signature
context_id=course-v1:Example+101+2023
context_label=Example101
context_title=Introduction to Example
launch_presentation_return_url=https://lms.example.com/return
lis_person_name_full=John Doe
lis_person_contact_email_primary=john.doe@example.com
custom_param1=value1
custom_param2=value2
