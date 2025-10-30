import re

def test_api_contract_template():
    required = {'case_id','name','email','date','amount'}
    payload = {'case_id':'TC001','name':'Alice','email':'alice@example.com','date':'2025-10-01','amount':120.5}
    assert required.issubset(payload.keys())
    assert re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', payload['email'])
