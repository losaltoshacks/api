from fastapi import APIRouter, HTTPException, Depends
from pyairtable.api.table import Table
from app.utilities import get_attendee_by_uuid, get_attendee_ref_by_email
from ..dependencies import get_mobile_table, get_firestore_client
from ..auth.auth_bearer import JWTBearer
from ..models.mobile_attendee import MobileAttendee, recordToMobileAttendee, firebaseToMobileAttendee

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

# get specific attendee
@router.get("/{email}")
async def get_attendee(email: str, firestore = Depends(get_firestore_client)):
    return firebaseToMobileAttendee(get_attendee_ref_by_email(email, firestore).get().to_dict())

# get attendee properties
@router.get("/{email}/checked_in")
async def check_attendee_checked_in(email: str, firestore = Depends(get_firestore_client)):
    return firebaseToMobileAttendee(get_attendee_ref_by_email(email, firestore).get().to_dict()).checked_in

@router.get("/{email}/meals")
async def get_attendee_meals(email: str, firestore = Depends(get_firestore_client)):
    return firebaseToMobileAttendee(get_attendee_ref_by_email(email, firestore).get().to_dict()).meals

@router.get("/{email}/meals/{meal}")
async def check_attendee_meal(email: str, meal: str, firestore = Depends(get_firestore_client)):
    return meal in firebaseToMobileAttendee(get_attendee_ref_by_email(email, firestore).get().to_dict()).meals

# update attendee properties
@router.post("/update/{email}/checked_in")
async def change_attendee_checked_in(email: str, checked_in: bool, firestore=Depends(get_firestore_client)):
    doc_ref = get_attendee_ref_by_email(email, firestore)
    try:
        res = "in" if checked_in else "out"
        doc_ref.update({"checked": res})
        return doc_ref.get().to_dict()["checked"]

    except:
        raise HTTPException(status_code=403, detail="Setting checked_in failed")

@router.post("/update/{email}/meals/add")
async def add_attendee_meals(email: str, meals: list[str], firestore=Depends(get_firestore_client)):
    doc_ref = get_attendee_ref_by_email(email, firestore)
    old_meals = firebaseToMobileAttendee(doc_ref.get().to_dict()).meals
    if len(old_meals) > 0 and old_meals[0] == "":
        old_meals = []
    new_meals = old_meals + [meal for meal in meals if meal not in old_meals and meal != ""]

    try:
        doc_ref.update({"meals": ",".join(new_meals)})
        return doc_ref.get().to_dict()["meals"]
    except:
        raise HTTPException(status_code=403, detail="Adding meals failed")
    
@router.post("/update/{email}/meals/remove")
async def remove_attendee_meals(email: str, meals: list[str], firestore=Depends(get_firestore_client)):
    doc_ref = get_attendee_ref_by_email(email, firestore)
    old_meals = firebaseToMobileAttendee(doc_ref.get().to_dict()).meals
    new_meals = [meal for meal in old_meals if meal not in meals and meal != ""]

    try:
        doc_ref.update({"meals": ",".join(new_meals)})
        return doc_ref.get().to_dict()["meals"]
    except:
        raise HTTPException(status_code=403, detail="Removing meals failed")