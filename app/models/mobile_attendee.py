from email.policy import default
from pydantic import BaseModel, Field

class MobileAttendee(BaseModel):
    email: str
    meals: list[str] = Field(default=[])
    checked_in: bool = Field(default=False)
    name: str
    dietary: str = Field(default="")

    def getAirtableFields(self):
        return self.dict(
        )

def firebaseToMobileAttendee(d):
    dietary = ""
    for i in d["form_response"]["answers"]:
        if i["field"]["id"] == "wC9PAqeg1XJX":
            dietary = i["text"]
    return MobileAttendee(
        email=d["form_response"]["answers"][2]["email"],
        checked_in=(d["checked"] == "in" if "checked" in d.keys() else False),
        meals=(d["meals"].split(",") if "meals" in d.keys() and d["meals"] != "" else []),
        name=d["form_response"]["answers"][0]["text"] + " " + d["form_response"]["answers"][1]["text"],
        dietary=dietary
    )

def recordToMobileAttendee(airtableRecord):
    fields = airtableRecord["fields"]
    return MobileAttendee(
        uuid=fields["UUID"],
        meals=(fields["meals"] if "meals" in fields.keys() else []),
        checked_in=(fields["checked_in"] if "checked_in" in fields.keys() else False),
        name=fields["Name"],
        dietary=(fields["Dietary Restrictions"] if "Dietary Restrictions" in fields.keys() else []),
        dietary_other=(fields["Dietary Other"] if "Dietary Other" in fields.keys() else "")
    )