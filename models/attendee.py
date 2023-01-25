from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass
from enum import Enum
from datetime import datetime
from fastapi import Query
from typing import Optional

# Helper Functions ===========
# listOfNames is an array containing the string values of an enum class, type is an Enum class
def strToEnumList(listOfNames, type):
    res = []

    for val in listOfNames:
        try: 
            res.append(type(val))
        except:
            continue # TODO: see if this ever gets called?   
    return res

def enumListToStringVals(listOfEnums):
    res = []

    for val in listOfEnums:
        try: 
            res.append(val.value)
        except:
            continue # TODO: see if this ever gets called?   
    return res

# Enums ======================
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

# Classes ====================
class Attendee(BaseModel):
    airtable_id: str | None = Field(default=None, alias="id")
    first_name: str = Field(alias="First Name")
    last_name: str = Field(alias="Last Name")
    email: str = Field(alias="Email")
    phone_number: str = Field(alias="Phone")
    gender: Gender = Field(alias="Gender")
    school: str = Field(alias="School")
    city: str = Field(alias="City")
    ethnicity: list[Ethnicity] = Field(alias="Ethnicity")
    ethnicity_other: str | None = None # TODO: figure out what this refers too
    date_of_birth: datetime = Field(alias="Date of Birth")
    dietary: list[DietaryRestriction] | None = Field(default=None, alias="Dietary Restrictions")
    dietary_other: str | None = None # TODO: figure out what this refers too
    t_shirt_size: ShirtSize = Field(alias="T-Shirt Size")
    contact: list[Contact] = Field(alias="How did you hear about us?")
    contact_other: str | None = None # TODO: figure out what this refers too
    parent_first_name: str = Field(alias="Parent/Guardian First Name")
    parent_last_name: str = Field(alias="Parent/Guardian Last Name")
    parent_email: str = Field(alias="Parent/Guardian Email Address")
    parent_phone: str = Field(alias="Parent/Guardian Phone Number")
    previous_hackathons: int = Field(alias="Number of Previous Hackathons Attended")
    experience: Experience = Field(alias="Programming Experience")
    device: bool = Field(alias="Access to Device")
    communications: bool = Field(alias="Share info with MLH?")
    github: str | None = Field(default=None, alias="GitHub")
    linkedin: str | None = Query(regex="^(http(s)?:\/\/)?([\w]+\.)?linkedin\.com\/(pub|in|profile)\/(.*)$", default = None, alias="LinkedIn")

    class Config:
        allow_population_by_field_name = True

    def getAirtableFields(self):
        fields_dict = self.dict(exclude={"airtable_id", "ethnicity_other","dietary_other","contact_other"}, by_alias=True)
        enum_list_fields = ["Ethnicity", "Dietary Restrictions", "How did you hear about us?"]
        for field_name in enum_list_fields:
            if field_name in fields_dict.keys() and fields_dict[field_name] != None:
                fields_dict[field_name] = enumListToStringVals(fields_dict[field_name])

        enum_fields = ["Gender", "T-Shirt Size"]
        for field_name in enum_fields:
            if field_name in fields_dict.keys() and fields_dict[field_name] != None:
                fields_dict[field_name] = fields_dict[field_name].value
        
        if "Date of Birth" in fields_dict.keys() and fields_dict["Date of Birth"] != None:
            fields_dict["Date of Birth"] = fields_dict["Date of Birth"].strftime("%Y-%m-%d")

        return fields_dict
    
# metaclass for converting all parameters into optional ones
class AllOptional(ModelMetaclass):
    def __new__(mcls, name, bases, namespaces, **kwargs):
        cls = super().__new__(mcls, name, bases, namespaces, **kwargs)
        for field in cls.__fields__.values():
            field.required=False
        return cls

# same as Attendee, but all parameters are optional
class UpdatedAttendee(Attendee, metaclass=AllOptional):
    # returns all fields that are not None
    def getUpdatedAirtableFields(self):
        fields_dict = self.getAirtableFields()
        stripped_fields_dict = {}
        for key, val in fields_dict.items():
            if val != None:
                stripped_fields_dict[key] = val
        
        return stripped_fields_dict

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
        dietary=strToEnumList(fields["Dietary Restrictions"], DietaryRestriction),
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

