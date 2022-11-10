import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "r") as file:
    f = file.read()
    print(type(f))
    print(f)

reponame = os.getenv("reponame")
print(reponame)

workspace_path = os.getenv("workspace_path")
print(workspace_path)
