import time

def test_api_validation_create_entity(base_url, api):
    # example：POST /api/v1/orders
    url = f"{base_url}/api/v1/orders"
    payload = {
        "customerName": "Alice",
        "age": 30,
        "startDate": "2026-01-05",
        "amount": "12.50",
    }

    r = api.post(url, json=payload, timeout=15)
    assert r.status_code in (200, 201), r.text

    data = r.json()
    assert "id" in data
    assert data["customerName"] == "Alice"

def test_end_to_end_workflow(base_url, api):
    """
    example E2E：
    1) create order
    2) submit order
    3) poll until status = APPROVED
    """
    create_url = f"{base_url}/api/v1/orders"
    submit_url = f"{base_url}/api/v1/orders/{{id}}/submit"
    get_url = f"{base_url}/api/v1/orders/{{id}}"

    # 1) create
    r = api.post(create_url, json={"customerName": "Bob", "age": 40, "startDate": "2026-01-05", "amount": "1.00"})
    assert r.status_code in (200, 201), r.text
    order_id = r.json()["id"]

    # 2) submit
    r = api.post(submit_url.format(id=order_id))
    assert r.status_code in (200, 202), r.text

    # 3) poll
    deadline = time.time() + 30
    last = None
    while time.time() < deadline:
        g = api.get(get_url.format(id=order_id))
        assert g.status_code == 200, g.text
        last = g.json()
        if last.get("status") in ("APPROVED", "COMPLETED"):
            break
        time.sleep(2)

    assert last is not None
    assert last.get("status") in ("APPROVED", "COMPLETED"), f"Final status unexpected: {last}"
