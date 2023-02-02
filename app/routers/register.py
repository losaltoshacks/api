import os
from ..auth.auth_handler import create_jwt
from postmarker.core import PostmarkClient
from ..models.attendee import Attendee
from fastapi import APIRouter, HTTPException, Depends, Request
from pyairtable.api.table import Table
from ..dependencies import get_table
from email_validator import validate_email, EmailNotValidError
from datetime import timedelta
import requests
import bisect

POSTMARK_SERVER_TOKEN = os.getenv("POSTMARK_SERVER_TOKEN")
BLACKLIST_PATH = os.getenv("BLACKLIST_PATH")
CLOUDFLARE_SECRET_KEY = os.getenv("CLOUDFLARE_SECRET_KEY")

router = APIRouter(
    prefix="/register",
    tags=["register"],
)

postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN, verbosity=3)


class EmailDomainValidator:
    def __init__(self):
        path = os.path.join(
            os.path.dirname(__file__), "../disposable_email_blocklist.txt"
        )
        with open(path) as fin:
            self.sorted_blacklist = tuple(fin.read().splitlines())

    def validate(self, email: str):
        index = bisect.bisect_left(self.sorted_blacklist, email)
        # Returns false if the domain is found in the blacklist, and true if not
        return not (
            index < len(self.sorted_blacklist) and self.sorted_blacklist[index] == email
        )


domain_validator = EmailDomainValidator()


@router.post("/attendee")
async def add_attendee(
    attendee: Attendee, request: Request, table: Table = Depends(get_table)
):
    # Check if the Cloudflare Turnstile token is valid
    turnstile = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": CLOUDFLARE_SECRET_KEY,
            "response": attendee.cf_turnstile_response,
        },
    )

    if not turnstile.json()["success"]:
        raise HTTPException(
            status_code=400, detail="Invalid Cloudflare Turnstile token."
        )

    # Check emails are valid
    try:
        email = validate_email(attendee.email, check_deliverability=True)
        attendee.email = email.ascii_email
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Your email address is not valid. {e}",
        )

    try:
        parent_email = validate_email(attendee.parent_email, check_deliverability=True)
        attendee.parent_email = parent_email.ascii_email
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Your parent/legal guardian's email address is not valid. {e}",
        )

    if not domain_validator.validate(
        email.ascii_domain
    ) or not domain_validator.validate(parent_email.ascii_domain):
        raise HTTPException(
            status_code=400,
            detail="Do not use temporary email addresses.",
        )

    # TODO: Cloudflare Turnstile

    # Verify both attendee and parent emails
    res = table.create(attendee.getAirtableFields())
    attendee_id = res["id"]

    # Tokens expire in 24 hours
    expire_delta = timedelta(minutes=1440)
    student_token = create_jwt(
        {"id": attendee_id, "type": "student"}, expires_delta=expire_delta
    )
    parent_token = create_jwt(
        {"id": attendee_id, "type": "parent"}, expires_delta=expire_delta
    )

    domain = request.url._url.removesuffix(request.url.path)

    # postmark.emails.send_with_template(
    #     TemplateAlias="email-verification",
    #     TemplateModel={
    #         "name": attendee.first_name,
    #         "action_url": f"{domain}/verify/{student_token}",
    #     },
    #     From="hello@losaltoshacks.com",
    #     To=attendee.email,
    # )

    # TODO: uncomment once testing is over
    # postmark.emails.send(
    #     From='hello@losaltoshacks.com',
    #     To=attendee.parent_email,
    #     Subject='Verify Los Altos Hacks Email',
    #     HtmlBody=f'Verify email: {domain}/verify/{student_token}' # TODO: make this an actual body
    #
    return res
