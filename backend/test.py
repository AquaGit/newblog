import requests

BASE = "http://127.0.0.1:5000/"


input()
response = requests.get(BASE + "article/2", {"views": 99})
print(response.json)
