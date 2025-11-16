'''
pip install requests python-dotenv
Create .env file
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxx
JIRA_PROJECT_KEY=ENG
'''
#!/usr/bin/env python3
"""
Jira automation script using requests
Python 3.9+
"""

import os
import base64
import requests
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL", "https://your-domain.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "you@example.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "ENG")

# --- Auth setup ---
auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()
auth_header = base64.b64encode(auth_string).decode()
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_header}"
}


def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task"):
    """Create a new Jira issue."""
    url = f"{JIRA_URL}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print(f"✅ Created issue {data['key']}")
    return data


def add_comment(issue_key: str, body: str):
    """Add a comment to a Jira issue."""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"
    payload = {"body": body}
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print(f"✅ Added comment to {issue_key}")
    return data


def search_issues(jql: str, max_results: int = 10):
    """Search Jira issues using JQL."""
    url = f"{JIRA_URL}/rest/api/3/search"
    payload = {"jql": jql, "maxResults": max_results}
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    for issue in data.get("issues", []):
        print(f"{issue['key']} - {issue['fields']['summary']} ({issue['fields']['status']['name']})")
    return data


def update_issue_priority(issue_key: str, priority: str):
    """Update the priority of a Jira issue."""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    payload = {"fields": {"priority": {"name": priority}}}
    resp = requests.put(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    print(f"✅ Updated {issue_key} priority to {priority}")


def assign_issue(issue_key: str, assignee_account_id: str):
    """Assign issue to a user (requires accountId in Jira Cloud)."""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/assignee"
    payload = {"accountId": assignee_account_id}
    resp = requests.put(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    print(f"✅ Assigned {issue_key} to account {assignee_account_id}")


def main():
    # 1) Create a new issue
    issue = create_issue(
        project_key=PROJECT_KEY,
        summary="Automated issue from Python",
        description="This issue was created via requests library script.",
        issue_type="Task"
    )
    issue_key = issue["key"]

    # 2) Add a comment
    add_comment(issue_key, "Investigating the issue. Logs will be attached shortly.")

    # 3) Search for issues
    search_issues(f'project = {PROJECT_KEY} ORDER BY created DESC')

    # 4) Update priority
    update_issue_priority(issue_key, "High")

    # 5) Assign issue (replace with real accountId from Jira Cloud)
    assign_issue(issue_key, "123456:abcdef")


if __name__ == "__main__":
    main()
