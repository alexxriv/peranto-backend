import json

import  urllib.parse as urlparse
from urllib.parse import urlencode
from auth import generate_authorization_code, verify_authorization_code, authenticate_client, authenticate_user_creentials, verify_client_info, generate_access_token, JWT_LIFE_SPAN

from fastapi import FastAPI, Request, Response, status

from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles


app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/auth")
def auth(request: Request, response: Response):
    client_id = request.query_params.get('client_id')
    redirect_uri = request.query_params.get('redirect_uri')
    
    if None in [client_id, redirect_uri]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_request'}
    
    if not verify_client_info(client_id, redirect_uri):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_client'}
    
    return templates.TemplateResponse("auth.html", {"request": request, "client_id": client_id, "redirect_uri": redirect_uri})


def process_redirect_url(redirect_url, authorization_code):

    # Prepare de redirect URL
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update({"authorization_code": authorization_code})
    url_parts[4] = urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url

@app.post("/signin")
def signin(request: Request, response: Response):
    username = request.form().get('username')
    password = request.form().get('password')
    client_id = request.form().get('client_id')
    redirect_uri = request.form().get('redirect_uri')

    if None in [username, password, client_id, redirect_uri]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_request'}
    
    if not verify_client_info(client_id, redirect_uri):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_client'}
    
    if not authenticate_user_creentials(username, password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_user_credentials'}
    
    authorization_code = generate_authorization_code(client_id, redirect_uri)

    redirect_url = process_redirect_url(redirect_uri, authorization_code)

    return RedirectResponse(url=redirect_url)


@app.post("/token")
def token(request: Request, response: Response):
    # Issues access token

    authorization_code = request.form.get('authorization_code')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    redirect_uri = request.form.get('redirect_uri')

    if None in [authorization_code, client_id, client_secret, redirect_uri]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_request'}
    
    if not authenticate_client(client_id, client_secret):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_client'}
    
    if not verify_authorization_code(authorization_code, client_id, redirect_uri):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'invalid_authorization_code'}
    
    access_token = generate_access_token()

    return json.dumps({
        'access_token': access_token.decode('utf-8'),
        "token_type": "JWT",
        "expires_in": JWT_LIFE_SPAN,
        })

