from pyairtable import Table
import os

async def get_table():
    AIRTABLE_KEY = os.getenv('AIRTABLE_KEY')
    BASE = os.getenv('BASE')
    TABLE = os.getenv('TABLE')
    
    table = Table(AIRTABLE_KEY, BASE, TABLE)

    return table