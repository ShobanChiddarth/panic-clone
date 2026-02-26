import sys
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

headers = {
    "Accept" : "application/vnd.github+json",
    "X-GitHub-Api-Version" : "2022-11-28",
    "Authorization" : os.environ.get("AUTHORIZATION_HEADER_VALUE")
}

url = "https://api.github.com/user"

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=4))
