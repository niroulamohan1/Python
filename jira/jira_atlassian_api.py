#!/usr/bin/env python3
"""
Jira automation using atlassian-python-api
pip install atlassian-python-api python-dotenv
"""

import os
from dotenv import load_dotenv
from atlassian import Jira


def main():
    load_dotenv()
    jira = Jira(
        url=os.getenv("JIRA_URL", ""),
        username=os.getenv("JIRA_EMAIL", ""),
        password=os.getenv("JIRA_API_TOKEN", ""),
        cloud=True,
    )

    project_key = os.getenv("JIRA_PROJECT_KEY", "ENG")

    # Create issue
    issue = jira.issue_create(fields={
        "project": {"key": project_key},
        "summary": "Automated issue via atlassian-python-api",
        "description": "Created by Python script.",
        "issuetype": {"name": "Task"},
    })
    issue_key = issue["key"]
    print(f"Created issue: {issue_key}")

    # Comment
    jira.issue_add_comment(issue_key, "Adding a comment via the library.")

    # Attachment
    jira.issue_attach_file(issue_key, "/tmp/metrics.csv")

    # Search
    res = jira.jql(f'project = {project_key} ORDER BY created DESC', limit=10)
    print(f"Found {len(res.get('issues', []))} issues")

    # Transition (example; transition id/name must exist)
    transitions = jira.get_transitions(issue_key)
    target = next((t for t in transitions if t["name"].lower() == "in progress"), None)
    if target:
        jira.set_transition(issue_key, transition=target["id"])
        print("Transitioned to In Progress")


if __name__ == "__main__":
    main()
