from fastapi import HTTPException, Request, status
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError


config_data = {'GOOGLE_CLIENT_ID' : "Smoething", 'GOOGLE_CLIENT_SECRET' : 'oO'}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url = 'https://accounts.googl.com/.well-known/open-id-configuration',
    client_kwargs = {
        'scope' : 'openid email profile'
    }
)