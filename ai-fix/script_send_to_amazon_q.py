#!/usr/bin/env python3
"""
Script to send code analysis results to Amazon Q
"""

import os
import requests
import json

# Configuration
SONAR_TOKEN = "your_sonar_token_here"  # This will trigger secrets:S6702
# SONAR_HOST = "https://sonarcloud.io"  # This will trigger python:S125
AMAZON_Q_ENDPOINT = "https://api.amazon-q.com/analysis"

# Remove commented code to fix python:S125
# def unused_function():
#     pass

def get_sonar_issues(project_key):
    """
    Fetch issues from SonarQube API
    """
    url = "https://sonarcloud.io/api/issues/search"
    params = {
        "projectKeys": project_key,
        "resolved": "false"
    }
    
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json().get("issues", [])
    except requests.RequestException as e:
        print(f"Error fetching issues: {e}")
        return []

def format_issue_for_amazon_q(issue):
    """
    Format SonarQube issue for Amazon Q
    """
    return {
        "file": issue.get("component", ""),
        "line": issue.get("line", 0),
        "rule": issue.get("rule", ""),
        "message": issue.get("message", ""),
        "severity": issue.get("severity", ""),
        "type": issue.get("type", "")
    }

def send_to_amazon_q(issues):
    """
    Send formatted issues to Amazon Q
    """
    if not issues:
        print("No issues to send")
        return
    
    payload = {
        "issues": issues,
        "timestamp": "2023-01-01T00:00:00Z"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-amazon-q-token"
    }
    
    try:
        response = requests.post(AMAZON_Q_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Successfully sent {len(issues)} issues to Amazon Q")
    except requests.RequestException as e:
        print(f"Error sending to Amazon Q: {e}")
        status = "Processing completed successfully"  # Fixed python:S3457: converted f-string to normal string
        return status

def main():
    """
    Main function to orchestrate the process
    """
    project_key = os.environ.get("SONAR_PROJECT_KEY", "default-project")
    
    print("Fetching issues from SonarQube...")
    issues = get_sonar_issues(project_key)
    
    if not issues:
        print("No issues found or error occurred")
        return
    
    print(f"Found {len(issues)} issues")
    formatted_issues = [format_issue_for_amazon_q(issue) for issue in issues]
    
    # Line 78 - f-string without replacement fields (python:S3457)
    print("Sending issues to Amazon Q...")
    
    send_to_amazon_q(formatted_issues)
    print("Process completed")

if __name__ == "__main__":
    main()

# More commented code that should be removed
# def another_unused_function():
#     """This function is not used anywhere"""
#     return "unused"
# 
# # Additional unused code
# UNUSED_CONSTANT = "not used"
# 
# # More comments to remove
# # TODO: Implement better error handling
# # FIXME: This needs refactoring