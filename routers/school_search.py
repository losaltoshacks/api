from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/school_search")
async def school_search(query: str):
    pass

# Return https://nces.ed.gov/globallocator/index.asp?search=1&State=&city=&zipcode=&miles=&itemname=Los+Altos+High+School&sortby=name&School=1&PrivSchool=1