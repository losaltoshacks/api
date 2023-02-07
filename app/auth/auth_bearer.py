from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sentry_sdk import capture_message
from ..auth.auth_handler import verify_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        # automatic error reportin
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                e = HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
                capture_message("Invalid authentication scheme.")
                raise e
            if not verify_jwt(credentials.credentials):
                e = HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
                capture_message("Invalid token or expired token.")
                raise e
            return credentials.credentials
        else:
            e = HTTPException(status_code=403, detail="Invalid authorization code.")
            capture_message("Invalid authorization code.")
            raise e
