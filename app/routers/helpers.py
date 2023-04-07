from fastapi import APIRouter, Depends
from pyairtable.api.table import Table
from app.dependencies import get_admissions_table, get_registration_table
from ..auth.auth_bearer import JWTBearer
import uuid

router = APIRouter(
    prefix="/helpers", tags=["helpers"], dependencies=[Depends(JWTBearer())]
)

# generates UUIDs for users without UUIDs in registration table
@router.post("/generateUUIDs/registration")
async def generate_uuids_reg(table: Table = Depends(get_registration_table)):
    for entry in table.all():
        if "UUID" not in entry["fields"].keys() or not entry["fields"]["UUID"]:
            generated_id = uuid.uuid4().hex
            table.update(entry["id"], {"UUID": generated_id})

# generates UUIDs for users without UUIDs in Guranteed Admissions table
@router.post("/generateUUIDs/admit")
async def generate_uuids_check_in(table: Table = Depends(get_admissions_table)):
    for entry in table.all():
        if "UUID" not in entry["fields"].keys() or not entry["fields"]["UUID"]:
            generated_id = uuid.uuid4().hex
            table.update(entry["id"], {"UUID": generated_id})