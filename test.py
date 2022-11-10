import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "r") as file:
    f = file.read()
    print(type(f))
    print(f)

t1 = os.getenv("reponame")
print("t1" + t1)

t2 = os.environ("reponame")
print("t2" + t2)
