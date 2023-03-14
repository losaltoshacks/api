from inspect import getmembers
from fastapi import APIRouter, Depends, Request
from pyairtable.api.table import Table
from ..dependencies import get_mobile_table
from ..auth.auth_bearer import JWTBearer
from ..models.mobile_attendee import recordToMobileAttendee

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

@router.get("/raw")
async def get_all_attendees_raw(request: Request, table: Table = Depends(get_mobile_table)):
    print(request.url._url.removesuffix(request.url.path))
    return table.all()