#!/usr/bin/env python3
"""
Script to send SonarQube issues to Amazon Q for AI-powered code analysis.
"""

import os
import requests
import json

SONAR_TOKEN = "your_sonar_token_here"  # Line 9 - secrets:S6702 violation

def fetch_sonar_issues():
    """Fetch issues from SonarQube API."""
    sonar_host = os.getenv("SONAR_HOST", "https://sonarcloud.io")
    project_key = os.getenv("SONAR_PROJECT_KEY")
    
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    
    params = {
        "projectKeys": project_key,
        "resolved": "false",
        "ps": 100
    }
    
    url = f"{sonar_host}/api/issues/search"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json().get("issues", [])

def send_to_amazon_q(issues):
    """Send issues to Amazon Q for analysis."""
    amazon_q_endpoint = os.getenv("AMAZON_Q_ENDPOINT")
    
    if not amazon_q_endpoint:
        print("Amazon Q endpoint not configured")
        return
    
    payload = {
        "issues": issues,
        "source": "sonarqube",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # Convert to JSON
    json_payload = json.dumps(payload)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('AMAZON_Q_TOKEN')}"
    }
    
    try:
        response = requests.post(amazon_q_endpoint, data=json_payload, headers=headers)
        response.raise_for_status()
        print("Successfully sent issues to Amazon Q")
    except requests.RequestException as e:
        print(f"Failed to send to Amazon Q: {e}")

def main():
    """Main function to orchestrate the process."""
    print("Fetching SonarQube issues...")
    issues = fetch_sonar_issues()
    print(f"Found {len(issues)} issues")
    
    print("Sending to Amazon Q...")
    send_to_amazon_q(issues)
    
    # This is an f-string without replacement fields
    message = f"Process completed successfully"  # Line 78 - python:S3457 violation
    print(message)

if __name__ == "__main__":
    main()