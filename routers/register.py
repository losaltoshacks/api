from fastapi import APIRouter, HTTPException, Depends
from models.attendee import Attendee
# from validate_email import validate_email
from pyairtable.api.table import Table
from dependencies import get_table

router = APIRouter(
    prefix="/register",
    tags=["register"]
)

# @router.post("/attendee", responses={201: {"description": "Attendee registered"}, 400: {"description": "Bad request"}})
# async def register_attendee(attendee: Attendee, table: Table = Depends(get_table)):
#     # Check emails are valid
#     if not validate_email(attendee.email):
#         raise HTTPException(status_code=400, detail="Email address is not valid. Please make sure you've typed your email correctly and aren't using a temporary email address.")
#     if not validate_email(attendee.parent_email):
#         raise HTTPException(status_code=400, detail="Parent email address is not valid. Please make sure you've typed the email correctly and aren't using a temporary email address.")

    # table.create(attendee.convert_to_airtable())

    # TODO: Verify both attendee and parent emails
    # TODO: Cloudflare Turnstile

