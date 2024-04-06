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

def get_attendee_ref_by_email(email: str, firestore):
    doc_ref = firestore.collection("messages").document(email)
    if doc_ref.get().exists:
        return doc_ref
    raise HTTPException(status_code=400, detail="No attendee with that email exists.")

# listOfNames is an array containing the string values of an enum class, type is an Enum class
def strToEnumList(listOfNames, type):
    res = []
    for val in listOfNames:
        try:
            res.append(type(val))
        except:
            continue  # TODO: see if this ever gets called?
    return res

# converts a list of enums to their string value equivalent
def enumListToStringVals(listOfEnums):
    res = []

    for val in listOfEnums:
        try:
            res.append(val.value)
        except:
            continue  # TODO: see if this ever gets called?
    return res