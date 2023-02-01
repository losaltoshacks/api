from re import A
from fastapi import APIRouter, HTTPException, Depends, Request
from pyairtable.api.table import Table
from models.attendee import Attendee, UpdatedAttendee
from models.attendee import recordToAttendee
from dependencies import get_table
from auth.auth_bearer import JWTBearer
from postmarker.core import PostmarkClient
from dotenv import load_dotenv
from os import getenv
from validate_email import validate_email
from auth.auth_handler import create_jwt

load_dotenv(override=True)

POSTMARK_SERVER_TOKEN = getenv("POSTMARK_SERVER_TOKEN")

router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
    dependencies=[Depends(JWTBearer())]
)

postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN, verbosity=3)

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

@router.post("/add")
async def add_attendee(attendee: Attendee, request: Request, table: Table = Depends(get_table)):
    # Check emails are valid
    # TODO: figure out why validate_email does not work
    if not validate_email(attendee.email):
        raise HTTPException(status_code=400, detail="Email address is not valid. Please make sure you've typed your email correctly and aren't using a temporary email address.")
    if not validate_email(attendee.parent_email):
        raise HTTPException(status_code=400, detail="Parent email address is not valid. Please make sure you've typed the email correctly and aren't using a temporary email address.")
    
    # Verify both attendee and parent emails
    res = table.create(attendee.getAirtableFields())
    attendee_id = res["id"]

    student_token = create_jwt({"id" : attendee_id, "type": "student"})
    parent_token = create_jwt({"id" : attendee_id, "type": "parent"})
    domain = request.url._url.removesuffix(request.url.path)

    # TODO: remove later - only for testing
    print(f"Verify student email: {domain}/verify/{student_token}")
    print(f"Verify parent email: {domain}/verify/{parent_token}")

    postmark.emails.send(
        From='team@losaltoshacks.com',
        To=attendee.email,
        Subject='Verify Los Altos Hacks Email',
        HtmlBody=f'Verify email: {domain}/verify/{student_token}' # TODO: make this an actual body
    )

    # TODO: uncomment once testing is over
    # postmark.emails.send(
    #     From='team@losaltoshacks.com',
    #     To=attendee.parent_email,
    #     Subject='Verify Los Altos Hacks Email',
    #     HtmlBody=f'Verify email: {domain}/verify/{student_token}' # TODO: make this an actual body
    #
    return res

@router.post("/update")
async def update_attendee(attendee_id: str, updated_attendee: UpdatedAttendee, table: Table = Depends(get_table)):
    try:
        return table.update(attendee_id, updated_attendee.getUpdatedAirtableFields())
    except:
        raise HTTPException(status_code=403, detail="Updating attendee failed")

# get specific attendee attribute
# field name is the name of the class variable for the Attendee class
@router.get("/{attendee_id}/{field_name}")
async def get_attendee_attribute(attendee_id: str, field_name: str, table: Table = Depends(get_table)):
    return getattr(recordToAttendee(table.get(attendee_id)), field_name)

# get specific attendee
@router.get("/{attendee_id}")
async def get_attendee(attendee_id: str, table: Table = Depends(get_table)):
    return recordToAttendee(table.get(attendee_id))