from fastapi import APIRouter

router = APIRouter(prefix="/api/offermart")

@router.get("/offers/{customer_id}")
def get_offers(customer_id: str):
    # simple static offers for demo
    return {
        "offers": [
            {"tenure_months":12, "interest_rate_percent":12},
            {"tenure_months":24, "interest_rate_percent":13},
            {"tenure_months":36, "interest_rate_percent":14}
        ]
    }
