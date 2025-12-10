from backend.apis import mock_crm

def verify_customer(customer_id: str):
    # uses sync helper from mock_crm
    c = mock_crm.get_customer_sync(customer_id)
    if c:
        return {"status":"verified","data":c}
    else:
        return {"status":"not_found"}
