import os

env_file = os.getenv("GITHUB_ENV")

with open(env_file, "r") as file:
    f = file.read()
    print(type(f))
    print(f)

# t1 = os.getenv()
# print(t1)

t2 = os.environ("${{ GITHUB_WORKSPACE }}")
print(t2)
