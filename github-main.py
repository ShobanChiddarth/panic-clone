import sys
import os
import subprocess
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv
import json


usernames = input("Enter GitHub usernames separated by space: ").split()
save_path = input("Enter dir path to save all repos (mass_clone_output): ") or "mass_clone_output"
depth = input("Enter depth (`None` for full history, 1 for just latest commit): ")

try:
    depth = eval(depth)
except Exception:
    sys.exit(1)

if not usernames:
    sys.exit(1)

load_dotenv()

GITHUB_API_BASE_URL = "https://api.github.com"

headers = {
    "Accept" : "application/vnd.github+json",
    "X-GitHub-Api-Version" : "2022-11-28",
    "Authorization" : os.environ.get("AUTHORIZATION_HEADER_VALUE")
}

session = requests.Session()
session.headers.update(headers)

def check_usernames_validity(usernames: list = usernames, session: requests.Session =session) -> dict:
    """
    Returns a dictionary in the following format:

    {
        "result": bool,
        "failing_users": list[str]
    }

    - `result` is True if all usernames are valid, otherwise False.
    - `failing_users` contains usernames that failed validation. This list is empty when `result` is True.
    """
    result = True
    failing_users = []
    for uname in usernames:
        user_url = urljoin(GITHUB_API_BASE_URL, "users", uname)
        response = session.get(user_url)
        if not response.ok:
            result = False
            failing_users.append(uname)
    
    return {
        "result": result,
        "failing_users": failing_users
    }

def fetch_all_repos(username: str, session: requests.Session = session) -> list:
    repos = []
    page = 1

    while True:
        repos_url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"
        params = {"per_page": 100, "page": page}
        response = session.get(repos_url, params=params)

        if not response.ok:
            print(f"[ERROR] Failed to fetch repos for {username}")
            sys.exit(1)

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

def clone_repo(clone_url: str, target_path: str, depth):
    if os.path.exists(target_path):
        print(f"[SKIP] {target_path} already exists")
        return

    cmd = ["git", "clone"]

    if depth is not None:
        cmd += ["--depth", str(depth)]

    cmd += [clone_url, target_path]

    print(f"[CLONING] {clone_url} -> {target_path}")

    process = subprocess.Popen(cmd)
    process.communicate()

    if process.returncode != 0:
        print(f"[SKIP] Failed cloning {clone_url}")
        return


uname_check_result = check_usernames_validity()

if uname_check_result["result"]:
    print("All usernames valid")
else:
    print("Failing users: " + " ".join(uname_check_result["failing_users"]))

os.makedirs(save_path, exist_ok=True)

for username in usernames:
    print(f"\n[USER] {username}")
    user_dir = os.path.join(save_path, username)
    os.makedirs(user_dir, exist_ok=True)

    repos = fetch_all_repos(username)
    for repo in repos:
        clone_url = repo.get("clone_url")
        repo_name = repo.get("name")
        if not clone_url or not repo_name:
            continue
        target_path = os.path.join(user_dir, repo_name)
        clone_repo(clone_url, target_path, depth)

print("\nDone.")
