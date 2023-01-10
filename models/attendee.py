from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from fastapi import Query

class Gender(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non-binary"
    other = "other"
    na = "na"

class ShirtSize(str, Enum):
    small = "s"
    medium = "m"
    large = "l"
    extra_large = "xl"

class Experience(str, Enum):
    none = "none"
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

class Ethnicity(str, Enum):
    aian = "aian"
    asian = "asian"
    black = "black"
    hispanic_latino = "hispanic-latino"
    pi = "pi"
    white = "white"
    other = "other"
    na = "na"

class DietaryRestriction(str, Enum):
    vegetarian = "vegetarian"
    vegan = "vegan"
    lactose_intolerant = "lactose_intolerant"
    gluten_intolerant = "gluten_intolerant"
    nut_allergy = "nut_allergy"
    other = "other"

class ContactMethod(str, Enum):
    instagram = "instagram"
    linkedin = "linkedin"
    twitter = "twitter"
    wom = "wom"
    prevhackathon = "prevhackathon"
    club = "club"
    teacher = "teacher"
    counselor = "counselor"
    other = "other"

class Attendee(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    gender: Gender
    school: str
    city: str
    ethnicity: list[Ethnicity]
    ethnicity_other: str
    date_of_birth: datetime
    dietary: list[DietaryRestriction] | None = None
    dietary_other: str
    t_shirt_size: ShirtSize
    contact: list[ContactMethod]
    contact_other: str
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
        for i in len(self.ethnicity):
            match self.ethnicity[i]:
                case Ethnicity.aian: self.ethnicity[i] = ""