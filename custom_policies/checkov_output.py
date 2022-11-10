import json
import os
import pandas as pd


## Functions ##


def sum_if_multiple(data):
    temp_passed = []
    temp_failed = []
    temp_skipped = []

    for cat in data:
        temp_passed.append(cat["passed"])
        temp_failed.append(cat["failed"])
        temp_skipped.append(cat["skipped"])

    return {
        "passed": sum(temp_passed),
        "failed": sum(temp_failed),
        "skipped": sum(temp_skipped),
    }


def extract_info_failed_checks(failed_checks, file_name):
    for check in failed_checks:
        temp = {
            "PostNL Repo": file_name,
            "Check ID": check["check_id"],
            "Description": check["check_name"],
            "AWS Resource": check["resource"],
            "File Path": check["file_path"],
            "URL": check["guideline"],
        }
        arr_checks.append(temp)  # Save information to array


# Create array of Checkov files in the json output folder
directory = "/Users/msloof/Documents/repos_checkov_output"
files = [f for f in os.listdir(directory) if f.endswith(".json")]

arr_checks = []
arr_summary = []

for file in files:  # Go through the Checkov files in the array
    file = os.path.join(directory, file)  # Reconstruct full file path

    # Save PostNL's repo name
    file_name = os.path.split(file)[1][:-5]

    with open(file, "r") as j:  # Open the file and read it as JSON file
        f = json.loads(j.read())
        if type(f) is list:
            temp_summary = []

            for i in range(len(f)):
                failed_checks = f[i]["results"]["failed_checks"]
                # Save information per failed check
                extract_info_failed_checks(failed_checks, file_name)

                temp_summary.append(f[i]["summary"])

            # Sum summary figures
            summary = sum_if_multiple(temp_summary)

        elif type(f) is dict:
            failed_checks = f["results"]["failed_checks"]

            # Save information per failed check
            extract_info_failed_checks(failed_checks, file_name)

            summary = f["summary"]

    # Calculate total number of checks performed by Checkov per repo
    total_checks = summary["passed"] + summary["failed"]

    # Save summary per PostNL repo to an array
    arr_summary.append(
        {
            "PostNL Repo": file_name,
            "Passed Checks": summary["passed"],
            "Failed Checks": summary["failed"],
            "Skipped Checks": summary["skipped"],
            "Total Checks": total_checks,
        }
    )

# Create index array starting from 1 for the Dataframe
index = range(1, len(arr_checks) + 1)

# Save the checks information to CSV file
df_checks = pd.DataFrame(arr_checks, index=index)
df_checks.to_csv(f"{directory}/checkov_failed_checks.csv", index=False)
print("checkov_failed_checks.csv has been created and saved")

# Save the summary information to CSV file
df_summary = pd.DataFrame(arr_summary)
print(df_summary)
df_summary.to_csv(f"{directory}/checkov_summary.csv", index=False)
print("checkov_summary.csv has been created and saved")
