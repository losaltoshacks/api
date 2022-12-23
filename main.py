from typing import Union
from fastapi import FastAPI

app = FastAPI()

# TODO:
# Endpoint for a registration form submission (with spam prevention with Cloudflare Turnstile)
#  - Adds a new row to Baserow
#  - Should also send a verification email using Postmark
# Endpoint for email verification
#  - Updates Baserow with confirmation that the email has been sent
# Endpoint for NCES school search for form submission
# Endpoint to get data from Baserow using a registrant's ID

