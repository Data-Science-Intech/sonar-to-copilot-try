#!/usr/bin/env python3
"""
SonarQube integration script for GitHub Actions
"""
import requests
import os
import json

# Configuration
SONAR_HOST = "https://sonarcloud.io"
SONAR_PROJECT_KEY = "Data-Science-Intech_sonar-to-copilot-try"
SONAR_TOKEN = "squ_4a8b9c3d2e1f0123456789abcdef012345678901"  # This should be in environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# Some commented code that should be removed
# HARDCODED_TOKEN = "squ_old_token_123"

def get_sonar_issues():
    """Fetch issues from SonarQube API"""
    headers = {
        'Authorization': f'Bearer {SONAR_TOKEN}'
    }
    
    url = f"{SONAR_HOST}/api/issues/search"
    params = {
        'componentKeys': SONAR_PROJECT_KEY,
        'resolved': 'false'
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def create_github_issue(issue_data):
    """Create a GitHub issue from SonarQube issue data"""
    # Implementation here
    pass

def main(project_key):
    """Main function to sync SonarQube issues to GitHub"""
    issues = get_sonar_issues()
    for issue in issues.get('issues', []):
        create_github_issue(issue)

if __name__ == "__main__":
    main("example_project")

# Some more commented code
# TODO: Remove this
# OLD_ENDPOINT = "https://old-api.sonarqube.com"

# print(f"Processing {len(issues)} issues")