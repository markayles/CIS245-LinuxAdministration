#
# This script dumps some network information and current connections to a file located in ~/networkdumps/. The folder will automatically be created if it does not already exist. A new file is created each time the command is run. No special parameters are needed. You can run this from any location.
#

import os 
from datetime import *

#Get the current date & time and format it for the file name
todayDate = datetime.today()
todayDate = todayDate.strftime("%d%b%Y-%H%M")

generatedFileSaveLocation = "~/networkdumps/"
generatedFileName = "NetworkInfoDump-" + todayDate
#Expanduser expands ~ to the full absolute path as python doesn't recognize ~
generatedFilePath = os.path.expanduser(generatedFileSaveLocation)
generatedFile = generatedFilePath + generatedFileName

characterCount = 40


def main():
    print("Network information dump generated: " + generatedFile)

    #Check if the directory exists, if not, create it
    if not os.path.exists(generatedFilePath):
        os.makedirs(generatedFilePath)

    #Create the file
    f = open(generatedFile, "a+")

    #print interfaces
    printInformation("ifconfig")

    #netstat stuff.. show current connections on ports
    printInformation("netstat")

    #dns info
    #printInformation("sed -n '/^[^#]/p' /etc/resolv.conf") #use this to hide the commented lines in file
    printInformation("cat /etc/resolv.conf")


    #Once everything is added to the file, just cat it out
    os.system("cat " + generatedFile)




def printInformation(commandToEnter):
    delim = "=" * characterCount

    os.system("echo " + delim + " >> " + generatedFile)
    os.system(commandToEnter + " >> " + generatedFile)
    os.system("echo " + delim + " >> " + generatedFile)



main()
