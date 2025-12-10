import json
from fastapi import APIRouter

router = APIRouter(prefix="/api/credit")

with open("backend/data/customers.json", "r") as f:
    _customers = json.load(f)

def get_score_sync(customer_id: str):
    for c in _customers:
        if c["customer_id"] == customer_id:
            return c.get("credit_score")
    return None

@router.get("/score/{customer_id}")
def get_score(customer_id: str):
    s = get_score_sync(customer_id)
    if s is not None:
        return {"credit_score": s}
    return {"message":"not found"}
