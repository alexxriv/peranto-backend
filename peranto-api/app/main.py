import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.auth import verify_access_token
from app.api.api_v1.api import api_router

app = FastAPI()

# middleware to authorize all requests

@app.middleware("http")
async def authorize(request, call_next):
    print("request.url.path: ", request.url.path)

    # Exclude docs and openapi from authorization
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        response = await call_next(request)
        return response
    print("request.headers: ", request.headers)
    # get the token from the request
    token = request.headers.get("authorization")

    print("token: ", token)
    # check if the token is valid
    if not token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    if 'Bearer' not in token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    # if the token is valid, call the next middleware
    
    access_token = token[7:]
    print("access_token: ", access_token)
    if access_token and verify_access_token(access_token):
        response = await call_next(request)
        
        return response
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

app.include_router(api_router)

# Post request to create a new user. User has a name and an email

