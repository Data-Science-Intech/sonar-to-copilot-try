#!/usr/bin/env python3
"""
AI Fix Script - Automated code analysis and fixing
"""

import os
# import sys
import requests
from requests.auth import HTTPBasicAuth

SONAR_TOKEN = "your_sonar_token_here"  # Line 11 - secrets issue
# This is some old configuration
# that we don't use anymore  # Line 13 - THIS IS THE ISSUE TO FIX
import json

def get_sonar_issues():
    """Fetch issues from SonarQube API"""
    host = os.environ.get("SONAR_HOST", "https://sonarcloud.io")
    project_key = os.environ.get("SONAR_PROJECT_KEY")
    
    api_url = f"{host}/api/issues/search"
    params = {
        "projectKeys": project_key,
        "resolved": "false",
        "ps": 100
    }
    
    auth = HTTPBasicAuth(SONAR_TOKEN, "")
    response = requests.get(api_url, params=params, auth=auth)
    response.raise_for_status()
    
    return response.json().get("issues", [])

def process_issues(issues, project_key):  # Line 38 - unused parameter
    """Process the SonarQube issues"""
    processed = []
    
    for issue in issues:
        processed_issue = {
            "file": issue.get("component", "").replace(f"{project_key}:", ""),
            "line": issue.get("line"),
            "rule": issue.get("rule"),
            "message": issue.get("message"),
            "severity": issue.get("severity")
        }
        processed.append(processed_issue)
    
    return processed

def create_github_issues(issues):
    """Create GitHub issues from SonarQube results"""
    github_token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    for issue in issues:
        title = f"[SonarQube] {issue['rule']} in {issue['file']}"
        body = f"""## Issue: {issue['message']}
**File:** `{issue['file']}`
**Line:** `{issue.get('line', 'N/A')}`
**Rule:** `{issue['rule']}`
**Severity:** `{issue.get('severity', 'Unknown')}`

> Auto-created from SonarQube analysis.
"""
        
        github_issue_url = f"https://api.github.com/repos/{repo}/issues"
        response = requests.post(github_issue_url, headers=headers, json={
            "title": title,
            "body": body,
            "labels": ["sonarqube", "auto-generated"]
        })
        
        if response.status_code == 201:
            print(f"✅ Created issue: {title}")
        elif response.status_code == 422:
            print(f"⚠️ Issue already exists: {title}")
        else:
            print(f"❌ Failed to create issue: {response.status_code}")

def main():
    """Main function"""
    try:
        print("🔍 Fetching SonarQube issues...")
        issues = get_sonar_issues()
        print(f"📦 Found {len(issues)} issues")
        
        project_key = os.environ.get("SONAR_PROJECT_KEY")
        processed_issues = process_issues(issues, project_key)
        
        print("🚀 Creating GitHub issues...")
        create_github_issues(processed_issues)
        
        print("✨ Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    # Legacy code that we might need later
    # print("This was used for debugging")
    # print("But we don't need it anymore")  # Line 98 - commented code issue
    
    return 0

if __name__ == "__main__":
    exit(main())