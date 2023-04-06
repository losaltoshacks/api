from fastapi import APIRouter, Depends, HTTPException
from pyairtable.api.table import Table
from pyairtable.formulas import match
from sentry_sdk import capture_message

from app.auth.auth_bearer import JWTBearer
from app.routers.attendees import update_attendee
from ..dependencies import get_table
from ..auth.auth_handler import verify_jwt, decode_jwt
from ..models.attendee import UpdatedAttendee, recordToAttendee

router = APIRouter(prefix="/verify", tags=["verify"])

@router.get("/discord", dependencies=[Depends(JWTBearer())])
async def verify_discord(email: str, disc_username: str, table: Table = Depends(get_table)):
    res = []
    for i in table.all(formula=match({"Email": email})):
        res.append(recordToAttendee(i))

    if len(res) == 0: 
        e = HTTPException(
            status_code=400,
            detail="No user with specified email found.",
        )
        capture_message("No user with specified email found.")
        raise e
    else:
        user = res[0] 
        if user.discord_id:
            e = HTTPException(
                status_code=400,
                detail="Discord username already set.",
            )
            capture_message("Discord username already set.")
            raise e

        try:
            table.update(user.airtable_id, {"Discord ID": disc_username})
        except:
            raise HTTPException(status_code=500, detail="Updating attendee failed")

    return f'Username {disc_username} sucessfully set'

@router.get("/{token}")
async def verify_email(token: str, table: Table = Depends(get_table)):
    # token is invalid or expired
    if not verify_jwt(token):
        e = HTTPException(
            status_code=403,
            detail="Expired or invalid verification link. Please try registering again!",
        )
        capture_message("Invalid or expired verification link.")
        raise e

    payload = decode_jwt(token)
    attendee_id = payload["id"]
    email_type = payload["type"]

    if not attendee_id or not email_type:
        # token does not contain payload id
        e = HTTPException(status_code=403, detail="Invalid verification link.")
        capture_message("Invalid verification link.")
        raise e

    field_name = "Parent Email Verified" if email_type == "parent" else "Email Verified"

    try:
        attendee = table.update(attendee_id, {field_name: True})

        parent_email_verified = (
            attendee["fields"]["Parent Email Verified"]
            if "Parent Email Verified" in attendee["fields"]
            else False
        )
        email_verified = (
            attendee["fields"]["Email Verified"]
            if "Email Verified" in attendee["fields"]
            else False
        )

        return {
            "parent_email_verified": parent_email_verified,
            "email_verified": email_verified,
        }
    except:
        # attendee does not exist
        e = HTTPException(status_code=403, detail="Invalid attendee ID.")
        capture_message("Invalid attendee ID.")
        raise e

