from pyairtable.formulas import match
from pyairtable.api.table import Table
from fastapi import HTTPException

# returns an attendee specified by their uuid
# if not found, raises a 400 HTTP exception
def get_attendee_by_uuid(attendee_uuid: str, table: Table):
    attendee = table.first(formula=match({"UUID": attendee_uuid}))
    if attendee == None:
        raise HTTPException(status_code=400, detail="No attendee with that ID exists.")
    return attendee