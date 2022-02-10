# File: UpdateMap.py
# By: Sebastian Alessandrino
# Date Created: 17/01/2022
# Purpose: To use the list of images on excel of the 3D map to update its data file accordingly

# Update: 29/01/2022
# Desc.: Will update the folder so that error handling is moved/improved and main program is called as a function
#        from ProjectGUI.py to allow for easier use

import pandas as pd
import os
from os import path
import csv
import UpdateMapFunctions as umf
import LoggingFunctions as lf

def performMapUpdate(mainDirPath, listPath, updDirPath, projectName):
    # Prepare data file of main tour for appending data of additional images
    umf.removeSettingsText(mainDirPath + "/app-files/data.js")

    # Create an empty list to be used later for determining which terms to replace in the main data.js file
    idToReplace = []

    # Create the logfile to be used in the program
    logFileName = lf.logInit(mainDirPath, listPath, updDirPath)

    # Start by removing old data
    actualListPath = makeCSVFromExcel(mainDirPath, listPath)
    with open(actualListPath) as list_file:
        list_images = list(csv.reader(list_file)) # Get the list of images
        list_images.pop(0) # Remove headings from the list
        
    tourImageList = os.listdir(mainDirPath + "/app-files/tiles/") # List of all image files
    ii = 0 # Iterator Variable
    while ii < len(list_images):
        foundImgData = False # Used to see if the image is in the main project
        jj = 0 # Iterator variable

        while not foundImgData and jj < len(tourImageList):
            if list_images[ii][2] == tourImageList[jj]: # If a matching ID is found...
                foundImgData = True
                list_images.pop(ii)
                tourImageList.pop(jj) # Remove found image from working list
            else: # Only increment if not found
                jj += 1
            
        if not foundImgData: # Only increment if the img is still in the list
            ii += 1

    # Get list data again as a result of 'popping' elements from the previous list
    with open(actualListPath) as list_file:
        list_images = list(csv.reader(list_file)) # Get the list of images
        list_images.pop(0) # Remove headings from the list

    # Remove all remaining data
    for oldImg in tourImageList:
        umf.removeOldImage(oldImg, mainDirPath)
        lf.logRemoveImage(logFileName, oldImg, listPath)
    # Produce a list of the images in the update directory and main directory and loop through them
    new_images = os.listdir(updDirPath + "/app-files/tiles/")
    existing_images = os.listdir(mainDirPath + "/app-files/tiles/")
    for new_img in new_images:
        # Need to first ensure that the image name is valid as per the given csv list file
        # The ID variables used for comparison do not consider the leading number as this will most likely be different
        imgValid = False
        newIDText = umf.getImageIDText(new_img)
        ii = 0 # Iterator Variable
        while ii < len(list_images) and not imgValid:
            if newIDText == umf.getImageIDText(list_images[ii][2]):
                imgValid = True
                newIDNum = int(list_images[ii][0])
            ii += 1

        if imgValid:
            # Check if new image already exists or not in MAIN_TOUR_DIR and act accordingly
            imgAlrExists = False
            if path.isdir(mainDirPath + "/app-files/tiles/" + str(newIDNum) + "-" + newIDText):
                imgAlrExists = True

            if imgAlrExists: # Replace existing image with new one
                validReplacement = umf.replaceImage(new_img, newIDNum, updDirPath, mainDirPath)
                idToReplace.append([new_img,list_images[newIDNum][2]])
                if validReplacement: # If image was a valid replacement for the pre-existing one
                    lf.logReplaceImage(logFileName, updDirPath, new_img, str(newIDNum) + "-" + newIDText)
                else:
                    lf.logHotspotsError(logFileName, updDirPath, new_img, str(newIDNum) + "-" + newIDText)
            else: # Add new image to main tour files
                umf.addNewImage(new_img, newIDNum, updDirPath, mainDirPath)
                idToReplace.append([new_img,list_images[newIDNum][2]])
                lf.logNewImage(logFileName, updDirPath, new_img, str(newIDNum) + "-" + newIDText)
        else:
            lf.logFormError(logFileName, umf.getNameFromIDText(newIDText), listPath)

    # Finishing touches to documents -> Settings replaced, identifier strings fixed, app menu updated
    umf.replaceSettingsText(mainDirPath + "/app-files/data.js", projectName)
    umf.correctAllIDs(idToReplace, mainDirPath + "/app-files/data.js")
    performMenuUpdate(listPath, mainDirPath, projectName, logFileName)
    delListCSVFile(actualListPath) # Delete temporary list csv file

    # Summarise the actions of the program in the Log File and determine what message to return to the user
    errorsOccurred = lf.logSummary(logFileName)
    return (logFileName, errorsOccurred)

# Function for updating the menu of the selected tour
def performMenuUpdate(listPath, dirPath, projectName, logFileName, onlyUpdateMenu=False):
    if onlyUpdateMenu:
        newLogFileName = lf.logInit(dirPath, listPath, 'N/A')

    actualListPath = makeCSVFromExcel(dirPath, listPath)
    with open(actualListPath) as listFile:
        listImages = list(csv.reader(listFile)) # Get the list of images
        listImages.pop(0) # Remove headings from the list
    delListCSVFile(actualListPath) # Delete temporary list csv file

    dataToPrioritise = umf.updateImageMenu(listImages, dirPath + "/app-files/index.html", projectName)
    umf.rearrangeDataFile(dataToPrioritise, dirPath + "/app-files/data.js", len(os.listdir(dirPath + "/app-files/tiles/")), projectName)
    # ^^^ To ensure that the data is ordered such that the menu works properly
    if not onlyUpdateMenu: # If updating rest of the map folder as well
        lf.logMenu(logFileName, dataToPrioritise)
        newLogFileName = logFileName # Purely for the purpose of returning the used logfile
    else:
        lf.logMenu(newLogFileName, dataToPrioritise)
    return newLogFileName

# Takes the input excel file and converts it to csv to be used in the program
def makeCSVFromExcel(mainDirPath, listPath):
    csvFileName = mainDirPath + '/tempList.csv'
    if not path.isfile(csvFileName):
        data = pd.read_excel(listPath, keep_default_na=False)
        data.to_csv(csvFileName, index=False)
    return csvFileName

# Checks that the given path exists and then deletes it
def delListCSVFile(csvPath):
    if path.isfile(csvPath):
        os.remove(csvPath)