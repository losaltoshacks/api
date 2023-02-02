from fastapi import FastAPI
from .routers import register, verify, attendees
from .auth import auth_handler
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

app.include_router(auth_handler.router)
app.include_router(register.router)
app.include_router(attendees.router)
app.include_router(verify.router)
