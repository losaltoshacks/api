from pyairtable.api.table import Table
import os
from dotenv import load_dotenv


async def get_table():
    load_dotenv()

    AIRTABLE_KEY = os.getenv("AIRTABLE_KEY", default="")
    BASE = os.getenv("BASE", default="")
    TABLE = os.getenv("TABLE", default="")

    table = Table(AIRTABLE_KEY, BASE, TABLE)

    return table
