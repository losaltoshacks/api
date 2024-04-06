from fastapi import APIRouter, HTTPException, Depends, Request
from pyairtable.api.table import Table
from pyairtable.formulas import match

from app.utilities import get_attendee_by_uuid
# from ..models.attendee import UpdatedAttendee
from ..models.attendee import recordToAttendee
from ..dependencies import get_registration_table, get_firestore_client
from ..auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/attendees", tags=["attendees"], dependencies=[Depends(JWTBearer())]
)


# get list of all attendees
@router.get("/")
async def get_all_attendees(table: Table = Depends(get_registration_table)):
    res = []
    for i in table.all():
        res.append(recordToAttendee(i))

    return res

@router.get("/raw")
async def get_all_attendees_raw(request: Request, table: Table = Depends(get_registration_table)):
    return table.all()


@router.post("/delete")
async def delete_attendee(attendee_id: str, table: Table = Depends(get_registration_table)):
    attendee_airtable_id = get_attendee_by_uuid(attendee_id, table)["id"]
    return table.delete(attendee_airtable_id)


# @router.post("/update")
# async def update_attendee(
#     attendee_id: str,
#     updated_attendee: UpdatedAttendee,
#     table: Table = Depends(get_registration_table),
# ):
#     attendee_airtable_id = get_attendee_by_uuid(attendee_id, table)["id"]
#     try:
#         return table.update(attendee_airtable_id, updated_attendee.getUpdatedAirtableFields())
#     except:
#         raise HTTPException(status_code=500, detail="Updating attendee failed")


# get specific attendee attribute
# field name is the name of the class variable for the Attendee class
@router.get("/{attendee_id}/{field_name}")
async def get_attendee_attribute(
    attendee_id: str, field_name: str, table: Table = Depends(get_registration_table)
):
    attendee = get_attendee_by_uuid(attendee_id, table)
    return getattr(recordToAttendee(attendee), field_name)


# get specific attendee
@router.get("/{email}")
async def get_attendee(email: str, firestore = Depends(get_firestore_client)):
    return firestore.collection('messages').document(email).get().to_dict()