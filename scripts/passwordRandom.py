import os
import string
import random

def generateRandomPassword(pwLength=8):
    sample = string.ascii_letters + string.digits
    pw = ''
    for i in range(pwLength):
        pw += random.choice(sample)
    return pw

for i in range(5):
    print("Password", i, generateRandomPassword())