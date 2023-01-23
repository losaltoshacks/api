from fastapi import APIRouter, HTTPException, Depends
from pyairtable.api.table import Table
from models.attendee import Attendee
from models.attendee import recordToAttendee
from dependencies import get_table

router = APIRouter(
    prefix="/attendees",
    tags=["attendees"]
)

# get specific attendee attribute
# field name is the name of the class variable for the Attendee class
@router.get("/{attendee_id}/{field_name}")
async def get_attendee_attribute(attendee_id: str, field_name: str, table: Table = Depends(get_table)):
    return getattr(recordToAttendee(table.get(attendee_id)), field_name)

# get specific attendee
@router.get("/{attendee_id}")
async def get_attendee(attendee_id: str, table: Table = Depends(get_table)):

    return recordToAttendee(table.get(attendee_id))

# get list of all attendees
@router.get("/")
async def get_all_attendees(table: Table = Depends(get_table)):
    res = []
    for i in table.all():
        res.append(recordToAttendee(i))

    return res

@router.get("/raw")
async def get_all_attendees_raw(table: Table = Depends(get_table)):
    return table.all()