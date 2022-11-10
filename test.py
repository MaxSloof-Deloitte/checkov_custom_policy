import os
import requests

# Retrieve complete repo and workspace path from GA env variables
repo_complete = os.getenv("repo_complete")
workspace_path = os.getenv("workspace_path")

# Split the complete repo into the app name
repo_app = repo_complete.split("/")[1]

# Create the full path for the Checkov output file
dir = f"{workspace_path}/results_json.json"

headers = {"Content-Type": "application/json"}

r = requests.put(
    f"https://iw6zajcn6i.execute-api.eu-central-1.amazonaws.com/tst/apigwdemo-max-2022/{repo_app}.json",
    headers=headers,
    data=dir,
)
