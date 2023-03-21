import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from auth import verify_access_token


app = FastAPI()

# middleware to authorize all requests

@app.middleware("http")
async def authorize(request, call_next):

    # Exclude docs and openapi from authorization
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        response = await call_next(request)
        return response
    # get the token from the request
    token = request.headers.get("Authorization")
    # check if the token is valid
    if not token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    if 'Bearer' not in token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    # if the token is valid, call the next middleware
    
    access_token = token[7:]

    if access_token and verify_access_token(access_token):
        response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    

@app.get("/users")
async def get_users():
    return [{"name": "John Doe"}, {"name": "Jane Doe"}]

