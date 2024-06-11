https://github.com/lepture/authlib
https://docs.authlib.org/en/latest/oauth/1/intro.html


## OAuth 1.0 Overview
OAuth 1.0a is a secure authorization protocol that enables third-party applications to interact with a user's account without exposing their password. The key components and steps involved in OAuth 1.0a are:

- Consumer (Client Application): The application attempting to access the user’s resources.
- Service Provider: The server hosting the user’s resources.
- User (Resource Owner): The owner of the resources the consumer wants to access.
- Consumer Key and Secret: Provided by the service provider to identify the consumer.
- Request Token and Secret: Temporary credentials used during the authorization process.
- Access Token and Secret: Credentials used by the consumer to access the user’s resources.

## OAuth 1.0a Flow
1) Obtaining a Request Token:
  - The consumer sends a request to the service provider to obtain a request token.
  - The service provider returns a request token and secret.
1) User Authorization:
  - The user is redirected to the service provider’s authorization URL.
  - The user authorizes the request token.
3) Exchanging Request Token for Access Token:
  - The consumer exchanges the authorized request token for an access token.
  - The service provider returns an access token and secret.
4) Accessing Protected Resources:
  - The consumer uses the access token to access protected resources on behalf of the user.
