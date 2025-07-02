#!/usr/bin/env python3
"""
Script to send SonarQube analysis results to Amazon Q for AI-powered code review.
This script safely handles authentication using environment variables.
"""

import os
import json
import requests
from typing import Dict, List, Optional

# Configuration from environment variables (secure approach)
AMAZON_Q_ENDPOINT = os.environ.get("AMAZON_Q_ENDPOINT")
AMAZON_Q_API_KEY = os.environ.get("AMAZON_Q_API_KEY")  # Use environment variable for API key
SONAR_HOST = os.environ.get("SONAR_HOST", "https://sonarcloud.io")
SONAR_TOKEN = os.environ.get("SONAR_TOKEN")  # Use environment variable for token
SONAR_PROJECT_KEY = os.environ.get("SONAR_PROJECT_KEY")


def validate_environment() -> bool:
    """Validate that all required environment variables are set."""
    required_vars = ["AMAZON_Q_ENDPOINT", "AMAZON_Q_API_KEY", "SONAR_TOKEN", "SONAR_PROJECT_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        return False
    return True


def fetch_sonar_issues() -> List[Dict]:
    """Fetch unresolved issues from SonarQube API."""
    if not SONAR_TOKEN:
        raise ValueError("SONAR_TOKEN environment variable not set")
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    api_url = f"{SONAR_HOST}/api/issues/search"
    params = {
        "projectKeys": SONAR_PROJECT_KEY,
        "resolved": "false",
        "ps": 100
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json().get("issues", [])
    except requests.RequestException as e:
        print(f"Error fetching SonarQube issues: {e}")
        return []


def send_to_amazon_q(issues: List[Dict]) -> bool:
    """Send issues to Amazon Q for AI analysis."""
    if not AMAZON_Q_API_KEY:
        raise ValueError("AMAZON_Q_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {AMAZON_Q_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "source": "SonarQube",
        "project": SONAR_PROJECT_KEY,
        "issues": issues,
        "timestamp": os.environ.get("BUILD_TIMESTAMP", "")
    }
    
    try:
        response = requests.post(
            AMAZON_Q_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        print(f"Successfully sent {len(issues)} issues to Amazon Q")
        return True
    except requests.RequestException as e:
        print(f"Error sending data to Amazon Q: {e}")
        return False


def main():
    """Main execution function."""
    print("Starting SonarQube to Amazon Q integration...")
    
    if not validate_environment():
        return 1
    
    print("Fetching SonarQube issues...")
    issues = fetch_sonar_issues()
    
    if not issues:
        print("No issues found or error occurred during fetch")
        return 0
    
    print(f"Found {len(issues)} issues, sending to Amazon Q...")
    success = send_to_amazon_q(issues)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())