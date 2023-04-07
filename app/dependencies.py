from pyairtable.api.table import Table
import os
from dotenv import load_dotenv

# registration table
async def get_table():
    load_dotenv()

    AIRTABLE_KEY = os.getenv("AIRTABLE_KEY", default="")
    BASE = os.getenv("BASE", default="")
    TABLE = os.getenv("TABLE", default="")

    table = Table(AIRTABLE_KEY, BASE, TABLE)

    return table

async def get_mobile_table():
    load_dotenv()

    AIRTABLE_KEY = os.getenv("AIRTABLE_KEY", default="")
    MOBILE_BASE = os.getenv("MOBILE_BASE", default="")
    MOBILE_TABLE = os.getenv("MOBILE_TABLE", default="")

    table = Table(AIRTABLE_KEY, MOBILE_BASE, MOBILE_TABLE)

    return table

# "Guaranteed Admissions" Table
async def get_admit_table():
    load_dotenv()

    AIRTABLE_KEY = os.getenv("AIRTABLE_KEY", default="")
    CHECK_IN_BASE = os.getenv("CHECK_IN_BASE", default="")
    ADMIT_TABLE = os.getenv("ADMIT_TABLE", default="")

    table = Table(AIRTABLE_KEY, CHECK_IN_BASE, ADMIT_TABLE)

    return table