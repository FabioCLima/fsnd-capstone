"""
Auth0 authentication utilities and @requires_auth decorator
"""
import json
import os
from functools import wraps
from urllib.request import urlopen

from jose import jwt
from flask import request, abort, g


class AuthError(Exception):
    """Standard Auth error wrapper to be JSON-serialized by error handlers."""

    def __init__(self, error, status_code):
        super().__init__(error)
        self.error = error
        self.status_code = status_code


# Environment configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
# Accept both names; prefer API_AUDIENCE per rubric/sample
API_AUDIENCE = os.getenv("API_AUDIENCE", os.getenv("AUTH0_AUDIENCE", ""))
ALGORITHMS = os.getenv("ALGORITHMS", "RS256").split(",")


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header."""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing", "description": "Authorization header is expected."}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header", "description": "Authorization header must start with Bearer."}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found."}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header", "description": "Authorization header must be Bearer token."}, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """Checks that the given permission is in the JWT payload."""
    if permission is None or permission == "":
        return True

    if "permissions" not in payload:
        raise AuthError({"code": "invalid_claims", "description": "Permissions not included in JWT."}, 400)

    if permission not in payload["permissions"]:
        raise AuthError({"code": "unauthorized", "description": "Permission not found."}, 403)

    return True


def verify_decode_jwt(token):
    """Verifies a JWT using Auth0 JWKS and returns the decoded payload."""
    if not AUTH0_DOMAIN or not API_AUDIENCE:
        raise AuthError({"code": "misconfigured", "description": "AUTH0_DOMAIN and API_AUDIENCE must be configured."}, 500)

    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        # Token malformado ou ilegível
        raise AuthError({"code": "invalid_header", "description": "Unable to parse authentication token."}, 400)

    if unverified_header.get("alg") == "HS256":
        # We expect RS256 tokens only
        raise AuthError({"code": "invalid_header", "description": "Invalid header. Use an RS256 signed JWT Access Token."}, 401)

    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError({"code": "invalid_header", "description": "Authorization malformed."}, 401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        raise AuthError({"code": "invalid_header", "description": "Unable to find the appropriate key."}, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "Token expired."}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"code": "invalid_claims", "description": "Incorrect claims. Check the audience and issuer."}, 401)
    except Exception:
        raise AuthError({"code": "invalid_header", "description": "Unable to parse authentication token."}, 400)


def requires_auth(permission=""):
    """Decorator to protect endpoints with Auth0 JWTs and optional permission check."""

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            # Attach payload to request context if needed downstream (Flask 3)
            g.current_user = payload
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator


