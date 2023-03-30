import requests

token = "A8st9R4yISnbu8z"
#url = f"http://192.168.1.4/message?token={token}"
url = f"http://172.20.10.14/message?token={token}"


def send(msg="Suspicious Intruders!!!"):
    data = {"title": "Home", "message": {msg}}
    requests.post(url, data)
