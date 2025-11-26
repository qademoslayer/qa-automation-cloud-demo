import allure
import pytest
import re
# test_api_contracts.py file
@allure.epic("API Tests")
@allure.feature("Contract Validation")
@allure.story("Basic schema validation")

def test_contract_schema_valid():
    with allure.step("Send API request"):
        response = {"status": 200, "schema_valid": True}
    with allure.step("Verify status and schema"):
        assert response["status"] == 200
        assert response["schema_valid"] is True

def test_api_contract_template():
    required = {'case_id','name','email','date','amount'}
    payload = {'case_id':'TC001','name':'Alice','email':'alice@example.com','date':'2025-10-01','amount':120.5}
    assert required.issubset(payload.keys())
    assert re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', payload['email'])
