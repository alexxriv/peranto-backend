import json
from pathlib import Path
import logging
import os
from typing import Annotated
from dotenv import load_dotenv

import  urllib.parse as urlparse
from urllib.parse import urlencode
from app.core.auth import ( authenticate_client, authenticate_user_credentials,
                  generate_access_token, generate_authorization_code, 
                  verify_authorization_code, verify_client_info,authorization_codes,
                  JWT_LIFE_SPAN)

from fastapi import FastAPI, Request, Response, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse


load_dotenv()

LOG_CONFIG_FILE = os.getenv("LOG_CONFIG_FILE")
# setup loggers
logging.config.fileConfig(LOG_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

#Create a User with UserCreate
@app.post("/signin", status_code=201)
async def signin(username: Annotated[str, Form()], password: Annotated[str, Form()], client_id: Annotated[str, Form()], redirect_url: Annotated[str, Form()]):
    
    logging.debug("Creating user, username: %s, client_id: %s, redirect_url: %s", username, client_id, redirect_url)

    if None in [username, password, client_id, redirect_url]:
        logging.debug("Invalid request")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "invalid_request"})
    
    if not verify_client_info(client_id, redirect_url):
        logging.debug("Invalid client")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "invalid_client"})
    
    if not authenticate_user_credentials(username, password):
        logging.debug("Invalid user credentials")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "invalid_user_credentials"})
    
    authorization_code = generate_authorization_code(redirect_url=redirect_url, client_id=client_id)

    logging.debug(authorization_codes)
    url = process_redirect_url(redirect_url, authorization_code)

    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)





@app.get("/auth")
def auth(request: Request, response: Response):
    client_id = request.query_params.get('client_id')
    redirect_url = request.query_params.get('redirect_url')
    
    if None in [client_id, redirect_url]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_request, client_id or redirect_url not provided'}
    
    if not verify_client_info(client_id, redirect_url):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_client, couldnt verify client id or redirect url'}
    
    return templates.TemplateResponse("auth.html", {"request": request, "client_id": client_id, "redirect_url": redirect_url})


def process_redirect_url(redirect_url, authorization_code):

    # Prepare de redirect URL
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update({"authorization_code": authorization_code})
    url_parts[4] = urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url


@app.post("/token")
def token(grant_type:Annotated[str, Form()],authorization_code: Annotated[str, Form()], client_id:Annotated[str, Form()], client_secret:Annotated[str, Form()], redirect_uri:Annotated[str, Form()]):
    # Issues access token
    logging.debug("Issuing access token, authorization_code: %s, client_id: %s, redirect_uri: %s", authorization_code, client_id, redirect_uri)
    if not authenticate_client(client_id, client_secret):
        logging.debug("Invalid client")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "invalid_client"})
    
    if not verify_authorization_code(authorization_code, client_id, redirect_uri):
        logging.debug("Invalid authorization code")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "invalid_client"})

    access_token = generate_access_token()
    logging.debug("Access token generated: %s", access_token)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "token_type": "JWT", "expires_in": JWT_LIFE_SPAN})
