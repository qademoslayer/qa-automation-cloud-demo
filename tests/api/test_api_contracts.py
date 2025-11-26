from utils.api_client import api_get

def test_demo_api_status():
    res = api_get("https://jsonplaceholder.typicode.com/todos/1")
    assert res.status_code == 200
