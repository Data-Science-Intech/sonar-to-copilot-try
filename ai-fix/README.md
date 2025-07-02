# AI-Fix Scripts

This directory contains scripts for automated code analysis and quality improvements.

## script.py

A SonarQube integration script that fetches code quality issues from SonarQube API.

### Environment Variables Required

- `SONAR_TOKEN`: Your SonarQube authentication token
- `SONAR_PROJECT_KEY`: The project key for SonarQube analysis
- `SONAR_HOST`: SonarQube server URL (defaults to https://sonarcloud.io)

### Usage

```bash
export SONAR_TOKEN="your_token_here"
export SONAR_PROJECT_KEY="your_project_key"
python script.py
```

### Security Note

This script properly uses environment variables for sensitive configuration like tokens. Never hardcode secrets in the source code.