from fastapi import APIRouter, Depends, HTTPException
from pyairtable.api.table import Table
from dependencies import get_table
from auth.auth_handler import verify_jwt, decode_jwt

router = APIRouter(
    prefix="/verify",
    tags=["verify"]
)

@router.get("/{token}")
async def verify__email(token: str, table: Table = Depends(get_table)):
    # token is invalid or expired
    if not verify_jwt(token):
        raise HTTPException(status_code=403, detail="Invalid or expired verification code.")
    
    payload = decode_jwt(token)
    attendee_id = payload["id"]
    email_type = payload["type"]

    if not attendee_id or not email_type:
        # token does not contain payload id
        raise HTTPException(status_code=403, detail="No payload id:: Invalid verification code.")
    
    field_name = "Parent Email Verified" if email_type == "parent" else "Email Verified"

    try:
        table.update(attendee_id, {field_name : True})
        return {"Email has successfully been verified!"}
    except:
        # attendee does not exist
        raise HTTPException(status_code=403, detail="Invalid verification code.")