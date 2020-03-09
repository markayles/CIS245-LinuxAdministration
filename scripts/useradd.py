#
# This script takes in a file containing real names of individuals and automatically generates a username and password for account creation. Name files should contain the full name of each individual on their own line. The groups listed in groups[] should be added prior to running script.
#
# To run this script enter: python useradd.py [names file]
#

import os
import sys
import re
import string
import random

#List of real names that will be added as users
namesToAdd = []
#Number of names that will be added
namesToAddCount = 0
#For printing out the current name currently being added
namesToAddCurrent = 1
#Groups to add users to
groups = ["admin", "developer", "staff", "temp"]
#For cycling through the groups when adding users
groupsAddIndex = 0
#Debugging/testing file that newly generated usernames will be added to. See method definition below for more information.
addedUsersFile = "addedusers.txt"


def main():
    global groupsAddIndex
    global namesToAddCurrent
    
    #Verify that there are more than 1 arguments. If yes, then read the 2nd argument, which should be a file name containing a list of names to create user accounts for. Each name should be placed in its own index within namesToAdd[]. If the file does not exist, quit the program and prompt user with the proper format.
    if len(sys.argv) > 1:
        print("Reading " + sys.argv[1])
        with open(sys.argv[1]) as f:
            namesToAdd = f.read().splitlines()
        namesToAddCount = len(namesToAdd)
    else:
        print("Please specify a file name as argument.")
        print("eg: python3 " + sys.argv[0] + " [names file]")
        quit()

    #Loop through the previously populated namesToAdd[].
    for x in namesToAdd:
        #Create a new list with each word in the person's name
        namePortions = x.split(" ")
        #Add the first letter of the first name to the username
        username = namePortions[0][0].lower()
        #Add the full last name to the username
        username += namePortions[len(namePortions) - 1].lower()
        #Subsitute any non-letter characters with nothing
        username = re.sub('[\W]', '', username)
        #Generate a random password from the method
        password = generateRandomPassword()
        
        #Check if username already exists. This is in a while loop in case the next generated username also exists, and so on.
        while checkIfUsernameExists(username):
            print("[ *USERNAME EXISTS - Appending number ] ")
            #Append a random single digit to end of username
            username += random.choice(string.digits)

        #Testing/debugging method to add newly generated username to a separate text file. See method definition below for more information.
        addUsernameToFile(username)

        #Start building a line to print out while adding the usernames
        printStatement = ""
        #Current user being added out of how many total we are adding
        printStatement += "("+str(namesToAddCurrent)+"/"+str(namesToAddCount)+")"
        #Full name along with username and password. Printing the password should be done in a more secure way, but for the sake of testing and assignment, we will just print to screen.
        printStatement += "Adding user " + x + " (" + username + ") pass: " + password
        print(printStatement)

        #Actually execute the command to add the user and add to a group specified in groups[]
        os.system("sudo useradd -G " + groups[groupsAddIndex] + " -m -c \"" + x + "\" " + username)
        #Change the password of the user
        os.system("echo \""+username+":"+password+"\" | sudo chpasswd")

        namesToAddCurrent += 1

        #Move the group index so the next user will be added to the next group in groups[]
        groupsAddIndex += 1
        #When we reach the last group in groups[], reset the index to 0 so we can cycle through the groups as we add users
        if groupsAddIndex >= len(groups):
            groupsAddIndex = 0



#Check if a username already exists by checking the passwd file
def checkIfUsernameExists(username):
    with open('/etc/passwd') as f:
        if username in f.read():
            return True
        else:
            return False

#For debugging/testing purposes and adding usernames to a separate text file so they could be removed with userdel.py. Simply so the script could be tested over and over without reverting to a previous snapshot of the virtual machine to remove newly added users.
def addUsernameToFile(username):
    with open(addedUsersFile, "a") as f:
        f.write(username + "\n")

#Generates a random password of letters and digits
def generateRandomPassword(pwLength=8):
    #Add letters and characters to the "pool" to choose from
    sample = string.ascii_letters + string.digits
    pw = ""
    for i in range(pwLength):
        #Choose a random item from the "pool"
        pw += random.choice(sample)
    return pw

main()