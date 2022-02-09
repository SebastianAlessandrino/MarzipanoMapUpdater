# File: UpdateMapFunctions.py
# By: Sebastian Alessandrino
# Date Created: 17/01/2022
# Purpose: Functions requiring for manipulating files and moving them between the new directory and the Main map directory

# Update: 07/02/2022
# Removed the requirement for having the same number of hotspots for one image that is replacing another

from re import L
import shutil
import os

# Returns the given ID string without the leading number
def getImageIDText(id):
    splitStr = id.split('-',1)

    if len(splitStr) == 2:
        outStr = splitStr[1]
    else:
        outStr = "N/A" 
    return outStr

# Converts ID text to the name that would be given when saving from the Marzipano Editor
def getNameFromIDText(id):
    outStr = ""
    splitStr = id.split('-')
    for i in range(len(splitStr)):
        outStr += splitStr[i]
        if not (i == len(splitStr) - 1):
            outStr += " "
    return outStr

# Checks if the new img is a valid replacement for the old one (has the same number and type of hotspots)
# Replaces data of the old image with that of the new one
def replaceImage(newImgID, newIDNum, sourceDir, destDir):
#    validReplacement = compareSimilarImageData(newImgID, str(newIDNum) + "-" + (newImgID.split('-',1))[1], sourceDir, destDir)
    validReplacement = True # Use above line if wishing for hotspot count of old images to have to equal that of new images before replacing

    if validReplacement:
        # Delete the original folder within the tiles folder
        shutil.rmtree(destDir + "/app-files/tiles/" + str(newIDNum) + "-" + getImageIDText(newImgID))

        # Copy over the tiles folder of the new image and edit it's name accordingly
        shutil.copytree(sourceDir + "/app-files/tiles/" + newImgID, destDir + "/app-files/tiles/" + str(newIDNum) + "-" + getImageIDText(newImgID))

        removeImageData(str(newIDNum) + "-" + (newImgID.split('-',1))[1], destDir + "/app-files/data.js")
        appendImageData(newImgID, sourceDir + "/app-files/data.js", destDir + "/app-files/data.js")
    return validReplacement

# Will copy and rename the folder containing image tiles of the new image from the new tour
# to the main tour
# Will also copy the relevent text of the data.js for the new images into the data.js file
# of the main tour
# Note that newImgID contains both the leading number and text
def addNewImage(newImgID, newIDNum, sourceDir, destDir):
    # Copy over the tiles folder of the new image and edit it's name accordingly
    shutil.copytree(sourceDir + "/app-files/tiles/" + newImgID, destDir + "/app-files/tiles/" + str(newIDNum) + "-" + getImageIDText(newImgID))

    appendImageData(newImgID, sourceDir + "/app-files/data.js", destDir + "/app-files/data.js")

# Will use removeImageData() to remove the main block of data attached to an image and also remove any link hotspots
# that relate to image data that is to be removed
def removeOldImage(oldImgID, mainDir):
    # Delete corresponding tiles folder for image to be removed
    shutil.rmtree(mainDir + "/app-files/tiles/" + oldImgID)

    # Remove main block of data in data.js file for image to be removed
    removeImageData(oldImgID, mainDir + "/app-files/data.js")

    # Remove hotspots referring to removed image
    with open(mainDir + "/app-files/data.js", 'r') as fr:
        lines = fr.readlines()
        printLine = True # True by default, only disabled in case of the hotspot being at the top, where "        }," should not be printed

        with open(mainDir + "/app-files/data.js.txt", 'w+') as fw:
            ii = 0 # Iterator Variable
            while ii < len(lines): # Go through every line in the file
                if ii < len(lines) - 5 and lines[ii+5].strip('\n') == f"          \"target\": \"{oldImgID}\"": # Found link
                    if lines[ii].strip('\n') == "      \"linkHotspots\": [" and lines[ii+6].strip('\n') == "        }": # Only one hotspot
                        fw.write("      \"linkHotspots\": [],\n")
                        ii += 8 # Go to start of info hotspots
                    elif lines[ii].strip('\n') == "      \"linkHotspots\": [" and lines[ii+6].strip('\n') == "        },": # Hotspot at top, more in list
                        fw.write(lines[ii]) # Line doesn't need to be changed
                        ii += 6 # Go to end of that entry
                        printLine = False # Don't want the "}," to be printed
                    elif lines[ii].strip('\n') == "        }," and lines[ii+6].strip('\n') == "        },": # Hotspot in between other hotspots
                        ii += 6 # Don't need to write to file, will write on next pass
                    elif lines[ii].strip('\n') == "        }," and lines[ii+6].strip('\n') == "        }": # Hotspot at end of list
                        ii += 6 # Don't need to write to file, will write on next pass
                else: # If not found link or in last few lines
                    if printLine:
                        fw.write(lines[ii])
                    ii += 1
                    printLine = True # Reset variable in case set to false

    os.remove(mainDir + "/app-files/data.js") # Remove the original file
    os.rename(mainDir + "/app-files/data.js.txt", mainDir + "/app-files/data.js") # Change the name of the new file to the original file's name

# Appends the data of the given newImgID to the end of the file at the given old file path (which should be a data.js file)
def appendImageData(newImgID, sourceFilePath, destFilePath):
    # Find the data entry for the given image in the new data.js file
    with open(sourceFilePath, 'r') as fr:
        lines = fr.readlines()
        foundData = False
        ii = 0 # Iteration Variable

        # Look for the correct entry
        while not foundData:
            if lines[ii].strip('\n') == f"      \"id\": \"{newImgID}\",":
                foundData = True
            else:
                ii += 1

        fileHasData = True # Assume true until found otherwise
        # Check if data.js file has no data in it
        with open(destFilePath, 'r') as fr:
            data = fr.readlines()
            if len(data) < 5:
                fileHasData = False

        # Append the found entry to the main data.js file
        with open(destFilePath, 'a') as fa:
            if fileHasData: # Data.js file has entries
                fa.write("    },\n    {\n")
            else: # Data.js file does not have entries
                fa.write("    {\n")
            while lines[ii].strip('\n') != "    }" and lines[ii].strip('\n') != "    },":
                fa.write(lines[ii])
                ii += 1

# Removes the data of a given imgID from the provided data.js file, does not remove hotspots
# Note that there are no checks for end of the data.js file as this function is only called if the data
# is already in the file
def removeImageData(imgID, filePath):
    with open(filePath, 'r') as fr:
        lines = fr.readlines()

        with open(filePath + ".txt", 'w+') as fw:
            atDataToRemove = False
            ii = 0 # Iterator Variable

            # Find data to remove
            while not atDataToRemove and ii < len(lines):
                if lines[ii].strip("\n") == "      \"infoHotspots\": []" or lines[ii].strip("\n") == "      ]" or lines[ii].strip("\n") == "var APP_DATA = {":
                    if lines[ii+3].strip("\n") == f"      \"id\": \"{imgID}\",":
                        atDataToRemove = True
                
                if atDataToRemove and lines[ii].strip("\n") == "var APP_DATA = {": # Special Case for start of file
                    fw.write(lines[ii]) # Write in scenes line
                    ii += 1
                
                fw.write(lines[ii])
                ii += 1

            # Iterate over remainder of file using previous iterator variable
            atEndOfRemDataList = False
            firstDataItemRemovedFailsafe = False

            if lines[ii-2].strip("\n") == "var APP_DATA = {": # Case for where first data element is removed
                firstDataItemRemovedFailsafe = True

            while ii < len(lines):
                if atEndOfRemDataList and firstDataItemRemovedFailsafe:
                    ii += 1 # Avoid writing in scenes line again
                    firstDataItemRemovedFailsafe = False
                if atEndOfRemDataList:
                    fw.write(lines[ii])
                else:
                    if lines[ii].strip("\n") == "      \"infoHotspots\": []" or lines[ii].strip("\n") == "      ]":
                        atEndOfRemDataList = True
                ii += 1
    
    os.remove(filePath) # Remove the original file
    os.rename(filePath + ".txt", filePath) # Change the name of the new file to the original file's name

# Used to remove the settings at the bottom of data.js files such that data for new images can be appended
# Copies all the lines of the given file barring the settings to a new file that is then used to replace the old one
def removeSettingsText(filePath):
    with open(filePath, 'r') as fr:
        lines = fr.readlines()

        ii = 0 # Iterator Variable
        with open(filePath + ".txt", 'w+') as fw:
            finalLine = False
            while not finalLine:
                if lines[ii].strip('\n') != "    }":
                    fw.write(lines[ii])
                    ii += 1
                else:
                    finalLine = True

    os.remove(filePath) # Remove the original file
    os.rename(filePath + ".txt", filePath) # Change the name of the new file to the original file's name

# Used to add the settings at the bottom of data.js files back afer using removeSettingsText()
def replaceSettingsText(filePath, projectName):
    with open(filePath, 'a') as datafile:
        datafile.write("    }\n")
        datafile.write("  ],\n")
        datafile.write(f"  \"name\": \"{projectName}\",\n")
        datafile.write("  \"settings\": {\n")
        datafile.write("    \"mouseViewMode\": \"drag\",\n")
        datafile.write("    \"autorotateEnabled\": false,\n")
        datafile.write("    \"fullscreenButton\": true,\n")
        datafile.write("    \"viewControlButtons\": true\n")
        datafile.write("  }\n};\n")

# Replaces the first element of each entry in replaceTerms with the second element of each entry at the given
# file path
def correctAllIDs(replaceTerms, filePath):
    for terms in replaceTerms:
        with open(filePath, 'r') as fr:
            data = fr.read()
            data = data.replace(f"\"{terms[0]}\"", f"\"{terms[1]}\"")

        with open(filePath, 'w') as fw:
            fw.write(data)

# Updates the sceneList component of the app's html file so that desired menus images
# are displayed on the menu as per the excel/csv file
def updateImageMenu(image_data_list, filePath, projectName):
    includedData = [] # List to keep the ID's of images in the menu
    with open(filePath, 'r') as fr:
        lines = fr.readlines()

        with open(filePath + ".txt", 'w+') as fw:
            atSceneList = False
            ii = 0 # Iterator Variable

            # Iterate until scenes section is found
            while not atSceneList and ii < len(lines):
                if lines[ii].strip('\n') == "  <ul class=\"scenes\">":
                    atSceneList = True
                if lines[ii].startswith('<title>'): # Insert correct title for file
                    fw.write(f'<title>{projectName}</title>\n')
                elif lines[ii].startswith('<body'): # <body> line must be set to multiple images for menu to display
                    fw.write('<body class=\"multiple-scenes view-control-buttons\">')
                else: # Print line normally
                    fw.write(lines[ii])
                ii += 1
            fw.write("\n")

            # Write in the selected menu options
            for data in image_data_list:
                if data[3] == 'y':
                    fw.write(f"      <a href=\"javascript:void(0)\" class=\"scene\" data-id=\"{data[2]}\">\n")
                    fw.write(f"        <li class=\"text\">{data[1]}</li>\n")
                    fw.write("      </a>\n\n")
                    includedData.append(data[2]) # Append the ID of the image in the menu
            
            # Iterate over remainder of file using previous iterator variable
            atEndOfSceneList = False

            while ii < len(lines):
                if atEndOfSceneList:
                    fw.write(lines[ii])
                else:
                    if lines[ii].strip('\n') == "  </ul>":
                        atEndOfSceneList = True
                        fw.write(lines[ii])
                ii += 1
    
    os.remove(filePath) # Remove the original file
    os.rename(filePath + ".txt", filePath) # Change the name of the new file to the original file's name

    return includedData

# Will rearrange the text in the file at the given path such that priority images (those that will be used in the menu)
# will have their data be at the top of the file
# This is required due to how the menu of the Marzipano tour works
# Note that totalImages and projectName are used for finalising this process
def rearrangeDataFile(dataToPrioritise, filePath, totalImages, projectName):
    lines = []
    with open(filePath, 'r') as fr:
        lines = fr.readlines()

    # Open main file which will become final data file, and temp file which will hold data until moved to main file
    with open(filePath + 'main.txt', 'w+') as fw_main:
        with open(filePath + 'temp.txt', 'w+') as fw_temp:
            ii = 0 # Iterator Variable
            firstEntry = True
            while ii < len(lines):
                jj = 0 # Iterator Variable 2
                if lines[ii].strip("\n") == "    {": # Start of a data entry
                    # Determine if detected entry is required or not
                    priorityData = False
                    while not priorityData and jj < len(dataToPrioritise):
                        if lines[ii+1].strip("\n") == f"      \"id\": \"{dataToPrioritise[jj]}\",":
                            priorityData = True
                        jj += 1
                        
                    # Write data to a file based on whether it is a priority or not
                    if priorityData:
                        if not firstEntry:
                            fw_main.write("    },\n")
                        while not (lines[ii].strip("\n") == "    }," or lines[ii].strip("\n") == "    }"):
                            fw_main.write(lines[ii])
                            ii += 1
                        firstEntry = False
                        ii += 1 # Increment again to skip '}' or '},' line
                    else:
                        fw_temp.write("    },\n")
                        while not (lines[ii].strip("\n") == "    }," or lines[ii].strip("\n") == "    }"):
                            fw_temp.write(lines[ii])
                            ii += 1
                        ii += 1 # Increment again to skip '}' or '},' line
                    
                elif lines[ii].strip("\n") == "  ],": # End of data entries
                    ii += 10 # Go past total line count, when this line is detected, only 8 remain
                else:
                    fw_main.write(lines[ii]) # This case occurs for start of file
                    ii += 1

        # Add non-priority data back to file and then settings text
        if not totalImages - len(dataToPrioritise) == 0:
            with open(filePath + 'temp.txt', 'r') as fr_temp:
                fw_main.write(fr_temp.read())
    replaceSettingsText(filePath + "main.txt", projectName)

    os.remove(filePath) # Remove the original file
    os.remove(filePath + "temp.txt") # Remove temp file
    os.rename(filePath + "main.txt", filePath) # Change the name of the new file to the original file's name

# Checks if two images have the same number and types of hotspots and returns True if they do or False if they don't
def compareSimilarImageData(newImgID, oldImgID, sourceDir, destDir):
    output = False
    newHotspots = countHotspots(newImgID, sourceDir + "/app-files/data.js")
    oldHotspots = countHotspots(oldImgID, destDir + "/app-files/data.js")

#    if newHotspots[0] == oldHotspots[0] and newHotspots[1] == oldHotspots[1]: # Use if also considering info hotspots
    if newHotspots == oldHotspots:
        output = True
    return output

# Does the hotspot counting for compareSimilarImageData()
def countHotspots(imgID, filePath):
    # Find out how many hotspots of each type there are in the image
    with open(filePath, 'r') as fr:
        lines = fr.readlines()
        linkHotspots = 0
#        infoHotspots = 0
        foundData = False
        ii = 0 # Iterator Variable
        while not foundData:
            if lines[ii].strip("\n") == f"      \"id\": \"{imgID}\",": # Correct data entry found, exit loop
                foundData = True
            ii += 1

        # Count link hotspots
        startOfLinks = False
        endOfLinks = False
        while not startOfLinks:
            if lines[ii].strip("\n") == "      \"linkHotspots\": [": # Link hotspots found, exit loop
                startOfLinks = True
            elif lines[ii].strip("\n") == "      \"linkHotspots\": []": # Case where there are no Link Hotspots, exit this loop and don't enter next one
                startOfLinks = True
                endOfLinks = True
            ii += 1

        while not endOfLinks:
            if lines[ii].strip("\n") == "        },": # Hotspot found, but not end of Link Hotspots
                linkHotspots += 1
            elif lines[ii].strip("\n") == "        }": # Last Link Hotspot found, exit loop
                linkHotspots += 1
                endOfLinks = True
            ii += 1
        
        # Count info hotspots -> This will occur immediately after link hotspots so only one while loop required
        # include if wanting the same number of info hotspots
#        endOfInfo = False
#        while not endOfInfo:
#            if lines[ii].strip("\n") == "        },": # Hotspot found, but not end of Info Hotspots
#                infoHotspots += 1
#            elif lines[ii].strip("\n") == "        }": # Last Info Hotspot found, exit loop
#                infoHotspots += 1
#                endOfInfo = True
#            elif lines[ii].strip("\n") == "      \"infoHotspots\": []": # Case where there are no hotspots
#                endOfInfo = True
#            ii += 1
#    return (linkHotspots, infoHotspots)
    return linkHotspots