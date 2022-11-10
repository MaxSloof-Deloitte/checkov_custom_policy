import os

env_file = os.getenv("GITHUB_ENV")
print(type(env_file))
print("\n" + env_file)
