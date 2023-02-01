import imp
from fastapi import FastAPI
from routers import register, school_search, verify, attendees
from auth import auth_handler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(register.router)
app.include_router(auth_handler.router)
app.include_router(school_search.router)
app.include_router(attendees.router)

# TODO:
# Endpoint for a registration form submission (with spam prevention with Cloudflare Turnstile)
#  - Adds a new row to Baserow
#  - Should also send a verification email using Postmark
# Endpoint for email verification
#  - Updates Baserow with confirmation that the email has been sent
# Endpoint for NCES school search for form submission
# Endpoint to get data from Baserow using a registrant's ID

