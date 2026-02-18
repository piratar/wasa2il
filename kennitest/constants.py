import os

ISSUER = os.getenv("ISSUER")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_SCOPE_NAME = os.getenv("API_SCOPE_NAME")
SCOPE = f"{os.getenv('SCOPE')} {API_SCOPE_NAME}"
APP_URL = os.getenv("APP_URL")
REDIRECT_URL = f"https://x.piratar.is/toy/response/"
ACCESS_TOKEN_AUDIENCE = f"{CLIENT_ID}-api"
