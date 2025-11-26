import requests

def api_get(url, headers=None):
    return requests.get(url, headers=headers)

def api_post(url, payload=None, headers=None):
    return requests.post(url, json=payload, headers=headers)
