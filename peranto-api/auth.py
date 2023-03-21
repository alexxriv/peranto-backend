import cryptography
import jwt
import logging
ISSUER = 'sample-auth-server'

with open('public.pem', 'rb') as f:
    public_key = f.read()

def verify_access_token(access_token):
    try:
        payload = jwt.decode(access_token, public_key, algorithms=['RS256'], issuer=ISSUER)
        logging.debug(payload)
        return True
    
    # Multiple exceptions can be raised by jwt.decode
    # We catch InvalidTokenError, ExpiredSignatureError, and DecodeError
    except jwt.exceptions.InvalidTokenError:
        return False