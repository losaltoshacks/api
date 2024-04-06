from fastapi import APIRouter, Depends, HTTPException
from pyairtable.api.table import Table
from pyairtable.formulas import match
from sentry_sdk import capture_message

from app.auth.auth_bearer import JWTBearer
from ..dependencies import get_mobile_table, get_registration_table, get_firestore_client
from ..auth.auth_handler import verify_jwt, decode_jwt
from app.utilities import get_attendee_by_uuid

router = APIRouter(prefix="/verify", tags=["verify"])


@router.get("/discord", dependencies=[Depends(JWTBearer())])
async def verify_discord(
    email: str, disc_username: str, firestore = Depends(get_firestore_client)
):
    doc_ref = firestore.collection("messages").document(email)
    doc = doc_ref.get()
    if not doc.exists:
        e = HTTPException(
            status_code=400,
            detail="No user with specified email found.",
        )
        capture_message("No user with specified email found.")
        raise e
    else:
        if "discord_id" in doc.to_dict():
            e = HTTPException(
                status_code=400,
                detail="Discord username already set.",
            )
            capture_message("Discord username already set.")
            raise e

        try:
            doc_ref.update({"discord_id": disc_username})
        except:
            raise HTTPException(status_code=500, detail="Updating attendee failed")

    first_name = doc.to_dict()["form_response"]["answers"][0]["text"]
    last_name = doc.to_dict()["form_response"]["answers"][1]["text"]
    return first_name, last_name


@router.get("/{token}")
async def verify_email(token: str, table: Table = Depends(get_registration_table)):
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
