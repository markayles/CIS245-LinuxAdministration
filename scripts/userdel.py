import os
import sys

namesToRemove = []
addedUsersFile = "addedusers.txt"

with open(addedUsersFile) as f:
    namesToRemove = f.read().splitlines()

for x in namesToRemove:
    print("Removing user " + x)
    os.system("sudo userdel -r " + x)