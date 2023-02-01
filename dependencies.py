from pyairtable.api.table import Table
import os

async def get_table():
    AIRTABLE_KEY = os.getenv('AIRTABLE_KEY', default="")
    BASE = os.getenv('BASE', default="")
    TABLE = os.getenv('TABLE', default="")

    table = Table(AIRTABLE_KEY, BASE, TABLE)

    return table
