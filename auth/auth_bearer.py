from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_handler import verify_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        # automatic error reportin
        super(JWTBearer, self).__init__(auto_error=auto_error) 
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
 
    
