from fastapi import APIRouter, Depends, Request
from pyairtable.api.table import Table
from ..dependencies import get_mobile_table
from ..auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/mobile", tags=["mobile"], dependencies=[Depends(JWTBearer())]
)

@router.get("/raw")
async def get_all_attendees_raw(request: Request, table: Table = Depends(get_mobile_table)):
    print(request.url._url.removesuffix(request.url.path))
    return table.all()