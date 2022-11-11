import requests
import json
import os

# FUNCTIONS


def extractInfoChecks(checks):

    # Go over every check and save the relevant information

    for check in checks:
        temp = {
            "Check ID": check["check_id"],
            "Description": check["check_name"],
            "AWS Resource": check["resource"],
            "File Path": check["file_path"],
            "URL": check["guideline"],
        }

        arr_checks.append(temp)  # Save information to array


def sumSummaryMultipleStacks(data):
    # If multiple stacks are synthesized in one repo, sum the summary figures
    temp_passed = []
    temp_failed = []
    temp_skipped = []
    temp_res_count = []

    for cat in data:
        temp_passed.append(cat["passed"])
        temp_failed.append(cat["failed"])
        temp_skipped.append(cat["skipped"])
        temp_res_count.append(cat["resource_count"])

    return {
        "passed": sum(temp_passed),
        "failed": sum(temp_failed),
        "skipped": sum(temp_skipped),
        "resource_count": sum(temp_res_count),
    }


###

# Retrieve complete repo and workspace path from GA env variables
repo_complete = os.getenv("repo_complete")
workspace_path = os.getenv("workspace_path")
# api_key = os.getenv("api_key")

# Split the complete repo into the app name
repo_app = repo_complete.split("/")[1]

# Create the full path for the Checkov output file
dir = f"{workspace_path}/results_json.json"

arr_checks = []
arr_summary = []

with open(dir, "r") as j:
    f = json.loads(j.read())

    if (
        type(f) is list
    ):  # Happens when multiple offerings are checked (CloudFormation and Hard-coded secrets).
        temp_summary = []

        for i in range(len(f)):  # For every stack:

            # Retrieve all the failed checks for evidence collection
            failed_checks = f[i]["results"]["failed_checks"]

            extractInfoChecks(failed_checks)

            # Save summary figures
            temp_summary.append(f[i]["summary"])

        # Sum all summary figures
        summary = sumSummaryMultipleStacks(temp_summary)

    elif type(f) is dict:  # Only CloudFormation are checked.

        # Retrieve all the failed checks for evidence collection
        failed_checks = f["results"]["failed_checks"]

        extractInfoChecks(failed_checks)

        # Save summary figures
        raw_sum = f["summary"]
        summary = {
            "passed": raw_sum["passed"],
            "failed": raw_sum["failed"],
            "skipped": raw_sum["skipped"],
            "resource_count": raw_sum["resource_count"],
        }

# Outline for the JSON file
dictionary = {
    "Status GitHub Repository": "Deployed",
    "Checkov Summary": summary,
    "Failed Checks": arr_checks,
}

json_object = json.dumps(dictionary, indent=4)

# Create and deliver the put request to the S3 bucket through the APIGW

apigw = f"https://iw6zajcn6i.execute-api.eu-central-1.amazonaws.com/tst/apigwdemo-max-2022/{repo_app}.json"
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key,
}
r = requests.put(
    apigw,
    headers=headers,
    data=json_object,
)

# Deliver confirmation message
print("------------\n\n")
print("The evidence has successfully been sent to the GRC Tool")
print("\n\n------------")
