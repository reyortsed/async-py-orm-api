from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
from app.common import config

# Identity provider config
TENANT_ID = config.get_env_or_secret("TENANT_ID")
API_APP_ID = config.get_env_or_secret("API_APP_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"

# Cache keys
JWKS = requests.get(JWKS_URL).json()

bearer_scheme = HTTPBearer()

def verify_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(k for k in JWKS["keys"] if k["kid"] == unverified_header["kid"])
      
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=API_APP_ID,
            issuer=f"{AUTHORITY}/v2.0"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    return verify_token(token)