from fastapi import APIRouter, Depends, HTTPException
from pyairtable.api.table import Table
from ..dependencies import get_table
from ..models.attendee import recordToAttendee
from ..auth.auth_handler import verify_jwt, decode_jwt

router = APIRouter(prefix="/verify", tags=["verify"])


@router.get("/{token}")
async def verify_email(token: str, table: Table = Depends(get_table)):
    # token is invalid or expired
    if not verify_jwt(token):
        raise HTTPException(
            status_code=403, detail="Invalid or expired verification link."
        )

    payload = decode_jwt(token)
    attendee_id = payload["id"]
    email_type = payload["type"]

    if not attendee_id or not email_type:
        # token does not contain payload id
        raise HTTPException(status_code=403, detail="Invalid verification link.")

    field_name = "Parent Email Verified" if email_type == "parent" else "Email Verified"

    try:
        attendee = table.update(attendee_id, {field_name: True})

        return {
            "parent_email_verified": attendee["fields"]["Parent Email Verified"],
            "email_verified": attendee["fields"]["Email Verified"],
        }
    except:
        # attendee does not exist
        raise HTTPException(status_code=403, detail="Invalid attendee ID.")
