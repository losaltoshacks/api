from fastapi import APIRouter, HTTPException, Depends, Request
from pyairtable.api.table import Table
from ..models.attendee import UpdatedAttendee
from ..models.attendee import recordToAttendee
from ..dependencies import get_table
from ..auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/attendees", tags=["attendees"], dependencies=[Depends(JWTBearer())]
)


# get list of all attendees
@router.get("/")
async def get_all_attendees(table: Table = Depends(get_table)):
    res = []
    for i in table.all():
        res.append(recordToAttendee(i))

    return res


@router.get("/raw")
async def get_all_attendees_raw(request: Request, table: Table = Depends(get_table)):
    print(request.url._url.removesuffix(request.url.path))
    return table.all()


@router.post("/delete")
async def delete_attendee(attendee_id: str, table: Table = Depends(get_table)):
    return table.delete(attendee_id)


@router.post("/update")
async def update_attendee(
    attendee_id: str,
    updated_attendee: UpdatedAttendee,
    table: Table = Depends(get_table),
):
    try:
        return table.update(attendee_id, updated_attendee.getUpdatedAirtableFields())
    except:
        raise HTTPException(status_code=403, detail="Updating attendee failed")


# get specific attendee attribute
# field name is the name of the class variable for the Attendee class
@router.get("/{attendee_id}/{field_name}")
async def get_attendee_attribute(
    attendee_id: str, field_name: str, table: Table = Depends(get_table)
):
    return getattr(recordToAttendee(table.get(attendee_id)), field_name)


# get specific attendee
@router.get("/{attendee_id}")
async def get_attendee(attendee_id: str, table: Table = Depends(get_table)):
    return recordToAttendee(table.get(attendee_id))
