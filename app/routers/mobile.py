from fastapi import APIRouter, Depends
from pyairtable.api.table import Table
from ..dependencies import get_mobile_table
from ..auth.auth_bearer import JWTBearer
from ..models.mobile_attendee import MobileAttendee, recordToMobileAttendee

router = APIRouter(
    prefix="/mobile", tags=["mobile"], dependencies=[Depends(JWTBearer())]
)

# get list of all attendees
@router.get("/")
async def get_all_attendees(table: Table = Depends(get_mobile_table)):
    res = []
    for i in table.all():
        res.append(recordToMobileAttendee(i))

    return res

# get raw data from airtable
@router.get("/raw")
async def get_all_attendees_raw(table: Table = Depends(get_mobile_table)):
    return table.all()

# add new attendee
@router.post("/add")
async def add_attendee(attendee: MobileAttendee, table: Table = Depends(get_mobile_table)):
    # TODO: add input verification?
    res = table.create(attendee.getAirtableFields())
    return res