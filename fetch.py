import json
import requests

# Set the GitHub Enterprise API endpoint
github_endpoint = 'https://githubent.kpit.com/api/v3'

# Set the repository path on the GitHub Enterprise instance
repository_path = '/repos/githubentuser1/CICD_Framework_and_KPI/commits'

# Set up authentication credentials for the GitHub Enterprise API
auth = ('githubentuser1', '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')

# Fetch the data from the GitHub Enterprise API
response = requests.get(github_endpoint + repository_path, auth=auth)

# Parse the response JSON data
data = response.json()

# Print each commit message to the console
for commit in data:
    message = commit['commit']['message']
    print(f"Commit Message: {message}")
    print(f"Message Length: {len(message)}")
    print("=" * 50)
