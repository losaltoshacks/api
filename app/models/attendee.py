from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass
from enum import Enum
from fastapi import Query


# Helper Functions ===========
# listOfNames is an array containing the string values of an enum class, type is an Enum class
def strToEnumList(listOfNames, type):
    res = []

    for val in listOfNames:
        try:
            res.append(type(val))
        except:
            continue  # TODO: see if this ever gets called?
    return res


def enumListToStringVals(listOfEnums):
    res = []

    for val in listOfEnums:
        try:
            res.append(val.value)
        except:
            continue  # TODO: see if this ever gets called?
    return res


# Enums ======================
class Grade(str, Enum):
    seventh = "7th Grade"
    eighth = "8th Grade"
    ninth = "9th Grade"
    tenth = "10th Grade"
    eleventh = "11th Grade"
    twelveth = "12th Grade"


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    non_binary = "Non-binary"
    other = "Not listed above"
    na = "Prefer not to answer"


class ShirtSize(str, Enum):
    small = "Small (S)"
    medium = "Medium (M)"
    large = "Large (L)"
    extra_large = "Extra Large (XL)"


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
    na = "Prefer not to answer"


class DietaryRestriction(str, Enum):
    vegetarian = "Vegetarian"
    vegan = "Vegan"
    lactose_intolerant = "Lactose Intolerant"
    gluten_intolerant = "Gluten Intolerant"
    nut_allergy = "Nut Allergy"


class Outreach(str, Enum):
    instagram = "Instagram"
    linkedin = "LinkedIn"
    twitter = "Twitter"
    wom = "Friend/Word-of-Mouth"
    prevhackathon = "Previous Hackathon"
    club = "Club"
    teacher = "Teachers"
    counselor = "School Counselor"


# Classes ====================
class Attendee(BaseModel):
    age: int = Field(alias="Age")
    airtable_id: str | None = Field(default=None, alias="id")
    # token: str = Field(alias="reCAPTCHA Token")
    dietary_restrictions_other: str | None = Field(default=None, alias="Other Dietary")
    dietary_restrictions: list[DietaryRestriction] | None = Field(
        default=None, alias="Dietary Restrictions"
    )
    email: str = Field(alias="Email")
    ethnicity_other: str | None = Field(default=None, alias="Other Ethnicity")
    ethnicity: list[Ethnicity] = Field(alias="Ethnicity")
    experience: Experience = Field(alias="Programming Experience")
    first_name: str = Field(alias="First Name")
    gender: Gender = Field(alias="Gender")
    github: str | None = Field(default=None, alias="GitHub")
    grade: Grade = Field(alias="Grade")
    hackathons: int = Field(alias="Number of Previous Hackathons Attended")
    last_name: str = Field(alias="Last Name")
    linkedin: str | None = Query(
        # regex="^(http(s)?:\/\/)?([\w]+\.)?linkedin\.com\/(pub|in|profile)\/(.*)$",
        default=None,
        alias="LinkedIn",
    )
    outreach_other: str | None = Field(default=None, alias="Other Outreach")
    outreach: list[Outreach] = Field(alias="Outreach Methods")
    parent_email: str = Field(alias="Parent/Guardian Email Address")
    parent_name: str = Field(alias="Parent/Guardian Name")
    parent_tel: str = Field(alias="Parent/Guardian Phone Number")
    school_name: str = Field(alias="School")
    school_address: str = Field(alias="School Address")
    shirt_size: ShirtSize = Field(alias="T-Shirt Size")
    tel: str = Field(alias="Phone")

    class Config:
        allow_population_by_field_name = True

    def getAirtableFields(self):
        fields_dict = self.dict(
            # exclude={"airtable_id", "token"},
            exclude={"airtable_id"},
            by_alias=True,
        )
        enum_list_fields = [
            "Ethnicity",
            "Dietary Restrictions",
            "Outreach Methods",
        ]
        for field_name in enum_list_fields:
            if field_name in fields_dict.keys() and fields_dict[field_name] is not None:
                fields_dict[field_name] = enumListToStringVals(fields_dict[field_name])

        enum_fields = ["Gender", "Grade", "T-Shirt Size"]
        for field_name in enum_fields:
            if field_name in fields_dict.keys() and fields_dict[field_name] is not None:
                fields_dict[field_name] = fields_dict[field_name].value

        return fields_dict


# metaclass for converting all parameters into optional ones
class AllOptional(ModelMetaclass):
    def __new__(mcls, name, bases, namespaces, **kwargs):
        cls = super().__new__(mcls, name, bases, namespaces, **kwargs)
        for field in cls.__fields__.values():
            field.required = False
        return cls


# same as Attendee, but all parameters are optional
class UpdatedAttendee(Attendee, metaclass=AllOptional):
    # returns all fields that are not None
    def getUpdatedAirtableFields(self):
        fields_dict = self.getAirtableFields()
        stripped_fields_dict = {}
        for key, val in fields_dict.items():
            if val is not None:
                stripped_fields_dict[key] = val

        return stripped_fields_dict


def recordToAttendee(airtableRecord):
    fields = airtableRecord["fields"]
    return Attendee(
        airtable_id=airtableRecord["id"],
        age=int(fields("Age")),
        outreach=strToEnumList(fields["Outreach Methods"], Outreach),
        outreach_other=(
            fields["Other Outreach"] if "Other Outreach" in fields.keys() else None
        ),
        dietary_restrictions=strToEnumList(
            fields["Dietary Restrictions"], DietaryRestriction
        ),
        dietary_restrictions_other=(
            fields["Other Dietary"] if "Other Dietary" in fields.keys() else None
        ),
        email=fields["Email"],
        ethnicity=strToEnumList(fields["Ethnicity"], Ethnicity),
        ethnicity_other=(
            fields["Other Ethnicity"] if "Other Ethnicity" in fields.keys() else None
        ),
        experience=Experience(fields["Programming Experience"]),
        first_name=fields["First Name"],
        gender=Gender(fields["Gender"]),
        github=(fields["GitHub"] if "GitHub" in fields.keys() else None),
        grade=Grade(fields["Grade"]),
        hackathons=int(fields["Number of Previous Hackathons Attended"]),
        last_name=fields["Last Name"],
        linkedin=(fields["LinkedIn"] if "LinkedIn" in fields.keys() else None),
        parent_email=fields["Parent/Guardian Email Address"],
        parent_name=fields["Parent/Guardian First Name"],
        parent_tel=fields["Parent/Guardian Phone Number"],
        school_name=fields["School"],
        school_address=fields["School Address"],
        shirt_size=ShirtSize(fields["T-Shirt Size"]),
        tel=fields["Phone"],
    )
