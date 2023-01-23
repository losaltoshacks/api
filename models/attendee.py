from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from fastapi import Query

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    non_binary = "Non-binary"
    other = "Not listed above"
    na = "Prefer not to answer"

class ShirtSize(str, Enum):
    small = "S"
    medium = "M"
    large = "L"
    extra_large = "XL"

class Experience(str, Enum):
    none = "None"
    beginner = "Beginner (< 6 months)"
    intermediate = "Intermediate (< 2 years)"
    advanced = "Advanced (< 5 years)"
    expert = "Expert (> 5 years)"

class Ethnicity(str, Enum):
    aian = "American Indian or Alaska Native"
    asian = "Asian"
    black = "Black or African American"
    hispanic_latino = "Hispanic or Latino"
    pacific_islander = "Native Hawaiian or Other Pacific Islander"
    white = "White"
    other = "other"
    na = ""

class DietaryRestriction(str, Enum):
    vegetarian = "Vegetarian"
    vegan = "Vegan"
    lactose_intolerant = "Lactose Intolerant"
    gluten_intolerant = "Gluten Intolerant"
    nut_allergy = "Nut allergy"
    other = "Other"

class Contact(str, Enum):
    instagram = "Instagram"
    linkedin = "LinkedIn"
    twitter = "Twitter"
    wom = "Friend/Word-of-Mouth"
    prevhackathon = "Previous Hackathon"
    club = "Club"
    teacher = "Teachers"
    counselor = "School Counselor"
    other = "other"


class Attendee(BaseModel):
    airtable_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    gender: Gender
    school: str
    city: str
    ethnicity: list[Ethnicity]
    ethnicity_other: str | None = None # TODO: figure out what this refers too
    date_of_birth: datetime
    dietary: list[DietaryRestriction] | None = None
    dietary_other: str | None = None # TODO: figure out what this refers too
    t_shirt_size: ShirtSize
    contact: list[Contact]
    contact_other: str | None = None # TODO: figure out what this refers too
    parent_first_name: str
    parent_last_name: str
    parent_email: str
    parent_phone: str
    previous_hackathons: int
    experience: Experience
    device: bool
    communications: bool
    github: str | None = None
    linkedin: str | None = Query(regex="^(http(s)?:\/\/)?([\w]+\.)?linkedin\.com\/(pub|in|profile)\/(.*)$", default = None)

    def convert_to_airtable(self):
        # Convert ethnicity to AirTable values
        # for i in len(self.ethnicity):
            # match self.ethnicity[i]:
                # case Ethnicity.aian: self.ethnicity[i] = ""
        pass;

# listOfNames is an array containing the string values of an enum class, type is an Enum class
def strToEnumList(listOfNames, type):
    res = []

    for val in listOfNames:
        try: 
            res.append(type(val))
        except:
            continue # TODO: see if this ever gets called?   
    return res

def recordToAttendee(airtableRecord):
    fields = airtableRecord["fields"]
    return Attendee(
        airtable_id=airtableRecord["id"],
        first_name=fields["First Name"],
        last_name=fields["Last Name"],
        email=fields["Email"],
        phone_number=fields["Phone"],
        gender=Gender(fields["Gender"]),
        school=fields["School"],
        city=fields["City"],
        ethnicity=strToEnumList(fields["Ethnicity"], Ethnicity),
        date_of_birth= datetime.strptime(fields["Date of Birth"], '%Y-%m-%d'),
        t_shirt_size=ShirtSize(fields["T-Shirt Size"]),
        contact=strToEnumList(fields["How did you hear about us?"], Contact),
        parent_first_name=fields["Parent/Guardian First Name"],
        parent_last_name=fields["Parent/Guardian Last Name"],
        parent_email=fields["Parent/Guardian Email Address"],
        parent_phone=fields["Parent/Guardian Phone Number"],
        previous_hackathons=int(fields["Number of Previous Hackathons Attended"]),
        experience=Experience(fields["Programming Experience"]),
        device="Access to Device" in fields.keys(),
        communications="Share info with MLH?" in fields.keys(),
        github=(fields["GitHub"] if "GitHub" in fields.keys() else None),
        linkedin=(fields["LinkedIn"] if "LinkedIn" in fields.keys() else None)
    )

