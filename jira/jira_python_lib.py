#!/usr/bin/env python3
"""
Jira automation with jira Python library
Python 3.9+
pip install jira python-dotenv
"""

import os
from dotenv import load_dotenv
from jira import JIRA

# Load credentials
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL", "https://your-domain.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "you@example.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "ENG")

# Connect
jira = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
)

# Create issue
issue_dict = {
    "project": {"key": PROJECT_KEY},
    "summary": "Disk space low on server abc",
    "description": "Root partition < 10% free space",
    "issuetype": {"name": "Bug"},
}
issue = jira.create_issue(fields=issue_dict)
print(f"✅ Created issue {issue.key}")

# Add comment
jira.add_comment(issue, "Cleanup initiated, monitoring disk usage.")

# Search issues
issues = jira.search_issues(f'project={PROJECT_KEY} AND status="To Do"', maxResults=5)
for i in issues:
    print(f"{i.key} - {i.fields.summary} ({i.fields.status.name})")
