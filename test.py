import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "r") as file:
    f = file.read()
    print(type(f))
    print(f)
