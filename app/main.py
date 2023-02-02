from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import register, verify, attendees
from .auth import auth_handler
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

origins = [
    "http://registration.losaltoshacks.com",
    "https://registration.losaltoshacks.com",
    "http://localhost",
    "http://localhost:8000",
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
