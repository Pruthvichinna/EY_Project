import json
from fastapi import APIRouter

router = APIRouter(prefix="/api/crm")

with open("backend/data/customers.json", "r") as f:
    _customers = json.load(f)

def get_customer_sync(customer_id: str):
    for c in _customers:
        if c["customer_id"] == customer_id:
            return c
    return None

@router.get("/customer/{customer_id}")
def get_customer(customer_id: str):
    c = get_customer_sync(customer_id)
    if c:
        return {"status":"success","data":c}
    return {"status":"error","message":"not found"}
