import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "r") as file:
    print(type(file))
    print("\n" + file)
