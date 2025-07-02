#!/usr/bin/env python3
"""
Script to send SonarQube analysis results to Amazon Q Developer for AI-powered code analysis.
This script demonstrates integration between SonarQube and Amazon Q.
"""

import os
import requests
SONAR_TOKEN = os.environ.get("SONAR_TOKEN")  # Fixed: Use environment variable instead of hardcoded token
# TODO: Remove hardcoded token and use environment variable
SONAR_HOST = os.environ.get("SONAR_HOST", "https://sonarcloud.io")
PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY", "your-project-key")

def get_sonar_issues(project_key):
    """Fetch issues from SonarQube API."""
    if not SONAR_TOKEN:
        raise ValueError("SONAR_TOKEN environment variable is required")
    
    auth = (SONAR_TOKEN, "")
    url = f"{SONAR_HOST}/api/issues/search"
    params = {
        "projectKeys": project_key,
        "resolved": "false",
        "ps": 100
    }
    
    response = requests.get(url, params=params, auth=auth)
    response.raise_for_status()
    return response.json().get("issues", [])

def send_to_amazon_q(issues):
    """Send issues to Amazon Q for analysis."""
    # This would integrate with Amazon Q API
    # For now, just print the issues
    print(f"Sending {len(issues)} issues to Amazon Q Developer...")
    for issue in issues:
        print(f"- {issue.get('component', 'Unknown')}: {issue.get('message', 'No message')}")

def main():
    """Main function to orchestrate the process."""
    try:
        print("Fetching SonarQube issues...")
        issues = get_sonar_issues(PROJECT_KEY)
        
        if issues:
            send_to_amazon_q(issues)
        else:
            print("No issues found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()