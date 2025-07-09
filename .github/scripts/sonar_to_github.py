import os
import subprocess
import requests
import json
import time

from requests.auth import HTTPBasicAuth



# SONAR_HOST_URL = "http://srvdpwfdev.odcdpw.ic:9000"
# SONAR_PROJECT_KEY = "dpw_foundation_dpw_foundation_api_common_bbb35689-94e3-47d2-bc66-0f2c8b1f4077"
# SONAR_TOKEN = os.gtenv("SONAR_TOKEN")
# $env:SONAR_TOKEN="sqp_8bd18b8f6118e26cd2e1fe9196704307e49fc043"
# SOURCE_DIR = "."
# ROOT_DIR = os.path.basename(os.getcwd())
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
SONAR_TOKEN = os.environ.get("SONAR_TOKEN")
SONAR_HOST = os.environ.get("SONAR_HOST")
SONAR_PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY")
SONAR_ORGANIZATION = os.environ.get("SONAR_ORGANIZATION")
REPO = os.environ.get("GITHUB_REPOSITORY") 
WORKSPACE = os.environ.get("GITHUB_WORKSPACE")  # Provided by GitHub Actions

github_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def ensure_target_classes_exists():
    path = os.path.join("target", "classes")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[📁] Created missing directory: {path}")
    else:
        print(f"[✅] Directory already exists: {path}")

def create_sonar_properties_file():
    content = f"""
sonar.organization={SONAR_ORGANIZATION}
sonar.projectKey={SONAR_PROJECT_KEY}
sonar.sources=.
sonar.host.url={SONAR_HOST}
sonar.login={SONAR_TOKEN}
sonar.java.binaries=target/classes
sonar.inclusions=**/*.py,**/*.java,**/*.js
sonar.exclusions=**/__pycache__/**,**/tests/**,target/**,ai-fix-agent/**, .github/**
""".strip()

    with open("sonar-project.properties", "w") as f:
        f.write(content)
    print("[📝] sonar-project.properties created successfully.")

def run_sonar_scanner_docker():
    print("[INFO] Running sonar-scanner via Docker...")

    cmd = [
        "docker", "run", "--rm",
                "-e", f"SONAR_TOKEN={SONAR_TOKEN}",
                "-v", f"{WORKSPACE}:/usr/src",
                "-w", "/usr/src",
                "sonarsource/sonar-scanner-cli"
    ]

    subprocess.run(cmd, check=True)
    print("[✅] Docker sonar-scanner completed.")

def fetch_issues(project_key, sonar_host_url):
    """
    Fetch all unresolved issues from SonarQube for the given project

    Args:
        project_key (str): SonarQube project key
        sonar_host (str): SonarQube host URL

    Returns:
        list: List of issue dictionaries containing file, line, message, and rule
    """
    # Get SonarQube token from environment
    # sonar_token = os.getenv("SONAR_TOKEN")
    # sonar_host = os.getenv("SONAR_HOST")
    # sonar_token = os.getenv("SONAR_TOKEN")
    if not SONAR_TOKEN:
        raise ValueError("SONAR_TOKEN environment variable not set")

    print(f"🔍 Fetching issues for project: {project_key}")

    # Setup authentication
    auth = HTTPBasicAuth(SONAR_TOKEN, "")

    try:
        # Make API request to fetch issues
        response = requests.get(
            f"{sonar_host_url}/api/issues/search",
            params={"componentKeys": project_key, "resolved": "false","severities": "CRITICAL"},
            auth=auth
        )

        # Check response status
        response.raise_for_status()

        # Parse response
        data = response.json()
        issues = data.get("issues", [])
        parsed_issues = []
        for issue in issues:
            parsed_issues.append({
                "file": issue["component"].split(":")[-1],
                "line": issue.get("line", 1),
                "message": issue["message"],
                "rule": issue["rule"]
            })

        with open("parsed_sonar_issues.json", "w") as f:
            json.dump(parsed_issues, f, indent=2)

        print(f"✅ Successfully fetched {len(parsed_issues)} issues")
        return parsed_issues
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching issues: {str(e)}")
        raise
# def paste_to_amazon_q():
#     print("[🤖] Activating Amazon Q panel in IntelliJ...")

#     # Give the user a chance to focus IntelliJ
#     time.sleep(3)
#     # Open Amazon Q sidebar (Alt+Shift+E), then Q tab (Alt+Shift+Q)
#     pyautogui.hotkey("altleft", "shiftleft", "e")
#     time.sleep(2)
#     pyautogui.hotkey("altleft", "shiftleft", "q")
#     time.sleep(3)  # Wait for Amazon Q panel to fully load
#     # Type message
#     pyautogui.write("@workspace Solve these issues", interval=0.05)
#     time.sleep(3)
#     pyautogui.hotkey("shift", "enter")
#     # Send the prompt line
#     time.sleep(3)
#     # Paste the clipboard content (assumes issues were copied there)
#     pyautogui.hotkey("ctrl", "v")
#     time.sleep(1)
#     pyautogui.press("enter")

#     print("[✅] Issues sent to Amazon Q.")

def submit_issues(issues):
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

if __name__ == "__main__":
    if not SONAR_TOKEN:
            raise ValueError("❌ SONAR_TOKEN is not set. Please export it before running.")
    ensure_target_classes_exists()
    create_sonar_properties_file()
    run_sonar_scanner_docker()
    issues = fetch_issues(SONAR_PROJECT_KEY, SONAR_HOST)
    # if issues:
    #     pyperclip.copy(json.dumps(issues, indent=2))
    #     paste_to_amazon_q()
    # else:
    #     print("[⚠️] No issues found.")
    if issues:
        submit_issues(issues)
    else:
        print("[⚠️] No issues found.")