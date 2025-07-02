#!/usr/bin/env python3
"""
Script to send code analysis results to Amazon Q for AI-powered insights.
This script processes SonarQube findings and sends them to Amazon Q for analysis.
"""

import os
import json
import requests
from typing import Dict, List, Any
from datetime import datetime

# Configuration constants
AMAZON_Q_ENDPOINT = "https://api.amazonq.aws.com/analyze"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
DEFAULT_SEVERITY_MAPPING = {
    "BLOCKER": "critical",
    "CRITICAL": "high", 
    "MAJOR": "medium",
    "MINOR": "low",
    "INFO": "info"
}

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {
        "api_key": os.environ.get("AMAZON_Q_API_KEY"),
        "project_name": os.environ.get("PROJECT_NAME", "unknown"),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "branch": os.environ.get("GITHUB_REF_NAME", "main"),
        "commit_sha": os.environ.get("GITHUB_SHA")
    }
    
    if not config["api_key"]:
        raise ValueError("AMAZON_Q_API_KEY environment variable is required")
    
    return config

def validate_sonar_data(data: Dict[str, Any]) -> bool:
    """Validate the structure of SonarQube data."""
    required_fields = ["issues", "projectKey"]
    
    for field in required_fields:
        if field not in data:
            print(f"Missing required field: {field}")
            return False
    
    if not isinstance(data["issues"], list):
        print("Issues field must be a list")
        return False
    
    return True

def format_issue_for_amazon_q(issue: Dict[str, Any]) -> Dict[str, Any]:
    """Format a SonarQube issue for Amazon Q analysis."""
    return {
        "rule": issue.get("rule", "unknown"),
        "severity": DEFAULT_SEVERITY_MAPPING.get(issue.get("severity", "INFO"), "info"),
        "component": issue.get("component", "unknown"),
        "line": issue.get("line"),
        "message": issue.get("message", ""),
        "type": issue.get("type", "CODE_SMELL"),
        "status": issue.get("status", "OPEN"),
        "creation_date": issue.get("creationDate"),
        "effort": issue.get("effort")
    }

def prepare_payload(config: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Prepare the payload for Amazon Q API."""
    formatted_issues = [format_issue_for_amazon_q(issue) for issue in issues]
    
    # Log preparation step
    print(f"Formatting issues for analysis")
    print(f"Processing configuration data") 
    print(f"Creating timestamp and metadata")
    # This is line 78 - the f-string without replacement fields that triggers python:S3457
    print(f"Prepared payload for Amazon Q analysis")
    
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "project": {
            "name": config["project_name"],
            "repository": config["repository"],
            "branch": config["branch"],
            "commit": config["commit_sha"]
        },
        "analysis": {
            "total_issues": len(formatted_issues),
            "issues": formatted_issues,
            "summary": generate_summary(formatted_issues)
        }
    }
    
    return payload

def generate_summary(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a summary of the issues."""
    severity_counts = {}
    type_counts = {}
    
    for issue in issues:
        severity = issue.get("severity", "info")
        issue_type = issue.get("type", "CODE_SMELL")
        
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
    
    return {
        "by_severity": severity_counts,
        "by_type": type_counts,
        "most_common_rules": get_most_common_rules(issues)
    }

def get_most_common_rules(issues: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    """Get the most common rules from the issues."""
    rule_counts = {}
    
    for issue in issues:
        rule = issue.get("rule", "unknown")
        rule_counts[rule] = rule_counts.get(rule, 0) + 1
    
    sorted_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
    
    return [
        {"rule": rule, "count": count}
        for rule, count in sorted_rules[:limit]
    ]

def send_to_amazon_q(payload: Dict[str, Any], config: Dict[str, Any]) -> bool:
    """Send the payload to Amazon Q API."""
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
        "User-Agent": "SonarQube-AmazonQ-Integration/1.0"
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                AMAZON_Q_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                print("Successfully sent data to Amazon Q")
                return True
            elif response.status_code == 429:
                print(f"Rate limited, attempt {attempt + 1}/{MAX_RETRIES}")
                continue
            else:
                print(f"API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
    
    return False

def main():
    """Main execution function."""
    try:
        # Load configuration
        config = load_config()
        print("Configuration loaded successfully")
        
        # Read SonarQube data from stdin or file
        if os.path.exists("sonar-report.json"):
            with open("sonar-report.json", "r") as f:
                sonar_data = json.load(f)
        else:
            print("Reading SonarQube data from stdin...")
            sonar_data = json.load(sys.stdin)
        
        # Validate data
        if not validate_sonar_data(sonar_data):
            print("Invalid SonarQube data format")
            return 1
        
        # Prepare and send payload
        payload = prepare_payload(config, sonar_data["issues"])
        
        if send_to_amazon_q(payload, config):
            print("Analysis sent to Amazon Q successfully")
            return 0
        else:
            print("Failed to send analysis to Amazon Q")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())