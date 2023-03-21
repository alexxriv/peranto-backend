import base64
import cryptography
import json
import jwt
import secrets
import time

from cryptography.fernet import Fernet


#KEY = Fernet.generate_key()
KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

ISSUER = 'sample_auth_server'
AUDIENCE = 'sample_auth_client'
CODE_LIFE_SPAN = 600
JWT_LIFE_SPAN = 1800

authorization_codes = {}

f = Fernet(KEY)

with open('private.pem', 'rb') as file:
    private_key = file.read()

def authenticate_user_creentials(username, password):
    return True

def authenticate_client(client_id, client_secret):
    return True

def verify_client_info(client_id, redirect_uri):
    return True

def generate_access_token():
    payload = {
        'iss': ISSUER,
        'aud': AUDIENCE,
        'iat': time.time(),
        'exp': time.time() + JWT_LIFE_SPAN,
    }
    return jwt.encode(payload, private_key, algorithm='RS256')


def generate_authorization_code(client_id, redirect_uri):

    #f = Fernet(KEY)
    authorization_code = f.encrypt(json.dumps({
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    }).encode('utf-8'))

    authorization_code = base64.urlsafe_b64encode(authorization_code, b'-_').decode('utf-8').replace('=', '')

    expiration_date = time.time() + CODE_LIFE_SPAN

    authorization_codes[authorization_code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "exp": expiration_date,
    }

    return authorization_code



def verify_authorization_code(authorization_code, client_id, redirect_uri):
    
    #f = Fernet(KEY)
    record = authorization_codes.get(authorization_code)
    if not record:
        return False
    
    client_id_in_record = record.get('client_id')
    redirect_uri_in_record = record.get('redirect_uri')
    expiration_date = record.get('exp')

    if client_id != client_id_in_record or redirect_uri != redirect_uri_in_record:
        return False
    
    if time.time() > expiration_date:
        return False
    
    del authorization_codes[authorization_code]
    return True