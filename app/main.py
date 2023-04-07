from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import helpers, mobile, register, verify, attendees
from .auth import auth_handler
from dotenv import load_dotenv
import sentry_sdk
import os

load_dotenv(override=True)

SENTRY_DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0.25,
)

app = FastAPI()

origins = [
    "http://register.losaltoshacks.com",
    "https://register.losaltoshacks.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_handler.router)
app.include_router(register.router)
app.include_router(attendees.router)
app.include_router(verify.router)
app.include_router(mobile.router)
app.include_router(helpers.router)