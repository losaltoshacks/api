from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from os import getenv
from pydantic import BaseModel
from sentry_sdk import capture_message
from dotenv import load_dotenv
import base64

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET", default="")
ALGORITHM = getenv("JWT_ALGORITHM", default="")
HASHED_PASSWORD = base64.b64decode(
    getenv("B64_HASHED_PASSWORD", default="failed").encode("ascii")
).decode("ascii")
USERNAME = getenv("LOGIN_USER")
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 1 week

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcfromtimestamp(decoded_token["exp"]) >= datetime.utcnow():
            return decoded_token
        else:
            return None
    except JWTError:
        return None


def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False

    try:
        payload = decode_jwt(jwtoken)
    except:
        payload = None
    if payload:
        isTokenValid = True
    return isTokenValid


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != USERNAME or not verify_password(
        form_data.password, HASHED_PASSWORD
    ):
        e = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        capture_message("Incorrect username or password")
        raise e

    access_token = create_jwt(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
