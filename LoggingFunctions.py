# File: LoggingFunctions.py
# By: Sebastian Alessandrino
# Date Created: 18/01/2022
# Purpose: Functions used to log the processes of UpdateMap.py in case of the need to see how the file was updated

from datetime import datetime
import os

# Creates a file for the log and writes a header into it
def logInit(mainTourPath, listFilePath, updateTourPath):
    date = str(datetime.now())
    day, time = date.split(' ')
    time = (time.split('.'))[0]
    timeStr = time.replace(':','-')
    logFileName = "LogFile_" + day + '_' + timeStr + ".txt"
    logFilePath = mainTourPath + "/Logfiles/" + logFileName

    if not os.path.isdir(mainTourPath + "/LogFiles/"): # If the logfile directory doesn't exist, make it
        os.mkdir(mainTourPath + "/LogFiles")

    with open(logFilePath, "w+") as fw:
        fw.write(f"MAP UPDATE LOGFILE @ {time} Date: {day}\n")
        fw.write("----------------------------------------------\n")
        fw.write(f"Updated File:    {mainTourPath}\n")
        fw.write(f"Image List File: {listFilePath}\n")
        fw.write(f"Input Data Dir.: {updateTourPath}\n")
        fw.write(f"\nCHANGES:\n")
    return logFilePath

# Appends a message stating an ID was added to the main tour
def logNewImage(logFile, updateTourName, oldID, newID):
    with open(logFile, 'a') as fa:
        fa.write(f"ADD IMAGE:     '{oldID}' from '{updateTourName}' ADDED to tour as: '{newID}'\n")

# Appends a message stating an ID was replaced in the main tour
def logReplaceImage(logFile, updateTourName, oldID, newID):
    with open(logFile, 'a') as fa:
        fa.write(f"REPLACE IMAGE: '{oldID}' from '{updateTourName}' WRITTEN OVER: '{newID}' with name: '{newID}'\n")

# Appends a message stating an old ID was removed from the main tour
def logRemoveImage(logFile, oldID, listFileName):
    with open(logFile, 'a') as fa:
        fa.write(f"REMOVE IMAGE:  '{oldID}' not found in '{listFileName}': REMOVED FROM TOUR\n")

# Appends an error message to the logfile if a new image was not recognised on the image list given
def logFormError(logFile, imageName, listFileName):
    with open(logFile, 'a') as fa:
        fa.write(f"FORM ERROR:    ID: '{imageName}' not found in '{listFileName}' NOT ADDED to tour\n")
        fa.write(f"               FIX: Ensure image names match those in spreadsheet!\n")

# Appends an error message if an image could not be replaced due to a disparity in hotspot count
def logHotspotsError(logFile, updateTourName, oldID, newID):
    with open(logFile, 'a') as fa:
        fa.write(f"REPLACE ERROR: '{oldID}' from '{updateTourName}' could not replace '{newID}' in tour. REASON: Differing Hotspot Counts\n")
        fa.write(f"               FIX: Add/Remove Hotspots to '{oldID}' data in 'data.js' of '{updateTourName}' or edit in Marzipano Tool and export again!\n")

# Appends a list of the menu items used in the most recent version of the project
def logMenu(logFile, dataToPrioritise):
    with open(logFile, 'a') as fa:
        fa.write(f"\nTOTAL MENU ITEMS: {len(dataToPrioritise)}\n")
        for data in dataToPrioritise:
            fa.write(f"MENU ADD: Image of ID: '{data}' INCLUDED in Tour Menu\n")

# Will summarise the processes that occurred in the program and notify the user if errors occurred
def logSummary(logFile):
    changes = 0
    adds = 0
    replaces = 0
    removes = 0
    errors = 0

    # Count statistics
    with open(logFile, 'r') as fr:
        lines = fr.readlines()

        for line in lines:
            lineText = line.split(':',1)
            if lineText[0] == "ADD IMAGE":
                adds += 1
                changes += 1
            elif lineText[0] == "REPLACE IMAGE":
                replaces += 1
                changes += 1
            elif lineText[0] == "REMOVE IMAGE":
                removes += 1
                changes += 1
            elif lineText[0] == "FORM ERROR" or lineText[0] == "REPLACE ERROR":
                errors += 1

    # Log Statistics
    with open(logFile, 'a') as fa:
        fa.write("\n\nSUMMARY:\n")
        fa.write(f"CHANGES:    {changes}\n")
        fa.write(f"ADDS:       {adds}\n")
        fa.write(f"REPLACES:   {replaces}\n")
        fa.write(f"REMOVES:    {removes}\n")
        fa.write(f"\nIMG ERRORS: {errors}\n")

    return errors