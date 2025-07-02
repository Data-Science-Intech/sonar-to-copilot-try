#!/usr/bin/env python3
"""
SonarQube integration script for analyzing code quality.
This script fetches issues from SonarQube and processes them.
"""

import os
import requests
from requests.auth import HTTPBasicAuth

SONAR_TOKEN = os.environ.get("SONAR_TOKEN")
SONAR_HOST = os.environ.get("SONAR_HOST", "https://sonarcloud.io")
SONAR_PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY")

def fetch_sonar_issues(project_key):
    """Fetch issues from SonarQube API."""
    if not SONAR_TOKEN:
        print("Error: SONAR_TOKEN environment variable not set")
        return []
        
    auth = HTTPBasicAuth(SONAR_TOKEN, "")
    
    sonar_api_url = f"{SONAR_HOST}/api/issues/search"
    params = {
        "projectKeys": project_key,
        "resolved": "false",
        "ps": 100
    }
    
    try:
        response = requests.get(sonar_api_url, params=params, auth=auth)
        response.raise_for_status()
        return response.json().get("issues", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SonarQube issues: {e}")
        return []

def main():
    """Main function to process SonarQube issues."""
    if not SONAR_PROJECT_KEY:
        print("Error: SONAR_PROJECT_KEY environment variable not set")
        return
    
    issues = fetch_sonar_issues(SONAR_PROJECT_KEY)
    print(f"Found {len(issues)} issues in SonarQube")
    
    for issue in issues:
        print(f"Issue: {issue.get('message', 'No message')}")
        print(f"File: {issue.get('component', 'Unknown')}")
        print(f"Rule: {issue.get('rule', 'Unknown')}")
        print("-" * 50)

if __name__ == "__main__":
    main()