import base64
import hashlib
import os
import urllib.parse
import webbrowser
import requests
from app.common import config

# Identity provider config
TENANT_ID = config.get_env_or_secret("TENANT_ID")
API_APP_ID = config.get_env_or_secret("API_APP_ID")
CLIENT_APP_ID = config.get_env_or_secret("CLIENT_APP_ID")
CLIENT_SECRET = config.get_env_or_secret("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"

# Callback URL for token request. 
# This must match exacly with one of the client app callback urls
# registered on identity provider.
# Controller is also in api atm, for simplicty
REDIRECT_URI = "https://localhost/callback" 

# Scope determines what permissions the client app will have to info from identity provider.
SCOPE = f"api://pythonapi_v2/access_as_user openid offline_access" 


# Workaround. Azure wouldnt give me a jwt without passing back an opaque token first
# Must generate PKCE verifier & challenge to retrieve an opaque token
def generate_pkce():
    verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b"=").decode("utf-8")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("utf-8")).digest()
    ).rstrip(b"=").decode("utf-8")
    return verifier, challenge

verifier, challenge = generate_pkce()

# The Auth Url we send our opaque token request to
auth_url = (
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_APP_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": SCOPE,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "12345"
    })
)

print("\nOpen the following URL in your browser and log in:")
print(auth_url)
webbrowser.open(auth_url)

# We get back an opaque token that then needs to be resent
code = input("\nPaste the opaque token from the redirect URL: ").strip()

# Request the jwt
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
data = {
    "client_id": CLIENT_APP_ID,
    "scope": SCOPE,
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
    "code_verifier": verifier,
}

resp = requests.post(token_url, data=data)
resp.raise_for_status()

tokens = resp.json()
print(tokens["access_token"]) # This can now be used to authorize client
