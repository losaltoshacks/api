from email.policy import default
from pydantic import BaseModel, Field

class MobileAttendee(BaseModel):
    airtable_id: str | None = Field(default=None)
    reg_id: str
    meals: list[str] = Field(default=[])
    signed_in: bool = Field(default=False)

    def getAirtableFields(self):
        return self.dict(
            exclude={"airtable_id"}
        )


def recordToMobileAttendee(airtableRecord):
    fields = airtableRecord["fields"]
    return MobileAttendee(
        airtable_id=airtableRecord["id"],
        reg_id=fields["reg_id"],
        meals=(fields["meals"] if "meals" in fields.keys() else []),
        signed_in=(fields["signed_in"] if "signed_in" in fields.keys() else False)
    )