#!/usr/bin/env python3
"""
Script for SonarQube integration and issue analysis.
This script demonstrates various SonarQube code quality issues.
"""

import os
# import requests  # Commented out import
import json
from typing import Dict, List

# sonar_token = "sqp_1234567890abcdef"  # Hardcoded token for demo
sonar_host = "https://sonarcloud.io"
# Another commented line for demo

def fetch_sonar_issues(host: str, token: str) -> List[Dict]:
    """Fetch issues from SonarQube API."""
    api_url = f"{host}/api/issues/search"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Mock response for demo
    return [
        {
            "key": "issue-1",
            "rule": "python:S1172",
            "message": "Remove unused parameter",
            "component": "ai-fix/script.py",
            "line": 38
        }
    ]

def process_issues(issues: List[Dict]) -> None:
    """Process and display SonarQube issues."""
    for issue in issues:
        print(f"Issue: {issue['message']}")
        print(f"Rule: {issue['rule']}")
        print(f"Location: {issue['component']}:{issue.get('line', 'N/A')}")

def analyze_project(host: str) -> Dict:
    """
    Analyze a SonarQube project and return results.
    """
    token = os.getenv("SONAR_TOKEN", "default-token")
    issues = fetch_sonar_issues(host, token)
    
    result = {
        "total_issues": len(issues),
        "host": host,
        "issues": issues
    }
    
    return result

def main():
    """Main function to run the analysis."""
    host = "https://sonarcloud.io"
    project = "my-project-key"
    
    # Call the function without the unused parameter
    results = analyze_project(host)
    
    print(f"Analysis complete. Found {results['total_issues']} issues.")
    process_issues(results['issues'])

if __name__ == "__main__":
    main()

# Some commented out legacy code
# def old_function():
#     """This function is no longer used."""
#     pass
#
# def another_old_function():
#     """Another deprecated function."""
#     return None

# Additional commented code block
# if __name__ == "__main__":
#     # Old main logic
#     old_function()
#     another_old_function()