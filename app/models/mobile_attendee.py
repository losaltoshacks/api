from email.policy import default
from pydantic import BaseModel, Field

class MobileAttendee(BaseModel):
    uuid: str
    meals: list[str] = Field(default=[])
    checked_in: bool = Field(default=False)
    name: str
    dietary: list[str] = Field(default=[])
    dietary_other: str = Field(default="")

    def getAirtableFields(self):
        return self.dict(
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