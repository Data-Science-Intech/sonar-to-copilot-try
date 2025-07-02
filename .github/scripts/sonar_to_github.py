import os
import requests
from requests.auth import HTTPBasicAuth

# Env from GitHub Actions
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# SONAR_TOKEN = os.environ.get("SONAR_TOKEN")
# SONAR_HOST = os.environ.get("SONAR_HOST", "https://sonarcloud.io")
# SONAR_PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY")
REPO = os.environ.get("GITHUB_REPOSITORY")

# Sanity check
# print(f"[ENV] Project: {SONAR_PROJECT_KEY}, Repo: {REPO}")

# # Headers
github_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
# auth = HTTPBasicAuth(SONAR_TOKEN, "")

# # Correct endpoint
# sonar_api_url = f"{SONAR_HOST}/api/issues/search"
# params = {
#     "projectKeys": SONAR_PROJECT_KEY,
#     "resolved": "false",
#     "ps": 100
# }

# print(f"[🔍] Fetching issues from {sonar_api_url}")
# response = requests.get(sonar_api_url, params=params, auth=auth)
# response.raise_for_status()
# issues = response.json().get("issues", [])
# print(f"[📦] Found {len(issues)} unresolved issues.")
issues = [
  {
    "file": "ai-fix/script.py",
    "line": 38,
    "rule": "python:S1172",
    "message": "Remove the unused function parameter \"project_key\"."
  },
  {
    "file": "ai-fix/script.py",
    "line": 7,
    "rule": "python:S125",
    "message": "Remove this commented out code."
  },
  {
    "file": "ai-fix/script.py",
    "line": 11,
    "rule": "secrets:S6702",
    "message": "Make sure this SonarQube token gets revoked, changed, and removed from the code."
  },
  {
    "file": "ai-fix/script.py",
    "line": 13,
    "rule": "python:S125",
    "message": "Remove this commented out code."
  },
  {
    "file": "ai-fix/script.py",
    "line": 98,
    "rule": "python:S125",
    "message": "Remove this commented out code."
  },
  # Security issue resolved: SonarQube token removed and environment variable used instead
  {
    "file": "ai-fix/script_send_to_amazon_q.py",
    "line": 78,
    "rule": "python:S3457",
    "message": "Add replacement fields or use a normal string instead of an f-string."
  },
  {
    "file": "try_cursor/settings.py",
    "line": 23,
    "rule": "secrets:S6687",
    "message": "Make sure this Django key gets revoked, changed, and removed from the code."
  }
]
# import os
# import requests
# from requests.auth import HTTPBasicAuth
# # from dotenv import load_dotenv
# # load_dotenv()

# # Config from environment
# # GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# # SONAR_TOKEN = os.getenv("SONAR_TOKEN")
# # SONAR_HOST = os.getenv("SONAR_HOST")
# # SONAR_PROJECT_KEY = os.getenv("SONAR_PROJECT_KEY")
# # REPO = os.getenv("GITHUB_REPOSITORY")  # Provided by GitHub Actions
# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# SONAR_TOKEN = os.environ.get("SONAR_TOKEN")
# SONAR_HOST = os.environ.get("SONAR_HOST")
# SONAR_PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY")
# REPO = os.environ.get("GITHUB_REPOSITORY")  # Provided by GitHub Actions

# # Headers
# github_headers = {
#     "Authorization": f"Bearer {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json"
# }
# auth = HTTPBasicAuth(SONAR_TOKEN, "")
# # Step 1: Get unresolved issues from SonarQube
# sonar_api_url = f"{SONAR_HOST}/api/issues/search"
# params = {
#     "projectKeys": SONAR_PROJECT_KEY,
#     "resolved": "false",
#     "ps": 100  # Max per page
# }

# print(f"[🔍] Fetching issues from {sonar_api_url}")
# response = requests.get(sonar_api_url, params=params, auth=auth)
# response.raise_for_status()
# issues = response.json().get("issues", [])
# print(f"Found {len(issues)} issues.")
# Step 2: Create GitHub issues for each
# for issue in issues:
#     title = f"[SonarQube] {issue['rule']} in {issue['component']}"
#     body = f"""## Issue: {issue['message']}
#     **Component:** `{issue['component']}`
#     **Severity:** `{issue['severity']}`
#     **Rule:** `{issue['rule']}`
#     **Line:** {issue.get('line', 'N/A')}
#     **Link:** {SONAR_HOST}/project/issues?id={SONAR_PROJECT_KEY}&issues={issue['key']}
#     > Auto-created from SonarQube analysis.
#     """

for issue in issues:
    title = f"[SonarQube] {issue['rule']} in {issue['file']}"
    body = f"""## Issue: {issue['message']}
               **File:** `{issue['file']}`
               **Line:** `{issue.get('line', 'N/A')}`
               **Rule:** `{issue['rule']}`

               > Auto-created from static analysis.
            """

    github_issue_url = f"https://api.github.com/repos/{REPO}/issues"
    res = requests.post(github_issue_url, headers=github_headers, json={
        "title": title,
        "body": body,
        "labels": ["sonarqube"]
    })


    if res.status_code == 201:
        print(f"[✅] GitHub issue created: {title}")
    elif res.status_code == 422 and "already_exists" in res.text:
        print(f"[⚠️] Duplicate issue: {title}")
    else:
        print(f"[❌] Failed to create issue: {res.status_code}, {res.text}")
