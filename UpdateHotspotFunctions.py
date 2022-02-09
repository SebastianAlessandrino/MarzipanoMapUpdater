# File: UpdateHotspotFunctions.py
# By: Sebastian Alessandrino
# Date Created: 02/02/2022
# Purpose: Hotspots required to perform operations on link and info hotspots in the map project

from InfoHotspot import InfoHotspot
from LinkHotspot import LinkHotspot
import os

# Finds the data entry of the given imageID in the data.js file of the chosen tour
# Will then store each of the found link hotspots as LinkHotspot objects and return them
# Note that no error checking is conducted as it is assumed the data.js file is in the correct format
def listLinkHotspots(dirPath, imgID):
    with open(dirPath + "/app-files/data.js", 'r') as fr:
        lines = fr.readlines()
        foundData = False
        ii = 0 # Iterator Variable
        while not foundData:
            if lines[ii].strip("\n") == f"      \"id\": \"{imgID}\",": # Correct data entry found, exit loop
                foundData = True
            ii += 1

        # Get to the start of the link hotspots section of the data
        foundLinks = False
        foundAllLinks = False
        initYaw = 0
        while not foundLinks:
            if lines[ii].strip("\n") == "      \"linkHotspots\": [":
                foundLinks = True
            elif lines[ii].strip("\n") == "      \"linkHotspots\": [],":
                foundLinks = True
                foundAllLinks = True
            elif lines[ii].startswith("      \"initialViewParameters\""):
                if lines[ii+1].startswith("        \"yaw\": "):
                    initYaw = float((lines[ii+1].removeprefix("        \"yaw\": ")).removesuffix(",\n"))
                    ii += 2
                elif lines[ii+1].startswith("        \"pitch\": "):
                    initYaw = float((lines[ii+2].removeprefix("        \"yaw\": ")).removesuffix(",\n"))
                    ii += 3
            else:
                ii += 1

        hotspots = []
        hotspotIDs = []
        # Loop through links if there are any
        while not foundAllLinks:
            if lines[ii].strip("\n") == "      ],":
                foundAllLinks = True
            elif lines[ii].startswith("          \"yaw\": "):
                yaw = float((lines[ii].removeprefix("          \"yaw\": ")).removesuffix(",\n"))
                pitch = float((lines[ii+1].removeprefix("          \"pitch\": ")).removesuffix(",\n"))
                target = (lines[ii+3].removeprefix("          \"target\": \"")).removesuffix("\"\n")

                hotspots.append(LinkHotspot(initYaw, yaw, pitch, target))
                hotspotIDs.append(target)
                ii += 4
            else:
                ii += 1
        return (hotspots, hotspotIDs, initYaw)

# Finds the data entry of the given imageID in the data.js file of the chosen tour
# Will then store each of the found info hotspots as InfoHotspot objects and return them
# Note that no error checking is conducted as it is assumed the data.js file is in the correct format
def listInfoHotspots(dirPath, imgID):
    with open(dirPath + "/app-files/data.js", 'r') as fr:
        lines = fr.readlines()
        foundData = False
        ii = 0 # Iterator Variable
        while not foundData:
            if lines[ii].strip("\n") == f"      \"id\": \"{imgID}\",": # Correct data entry found, exit loop
                foundData = True
            ii += 1

        # Get to the start of the info hotspots section of the data
        foundInfo = False
        foundAllInfo = False
        initYaw = 0
        while not foundInfo:
            if lines[ii].strip("\n") == "      \"infoHotspots\": [":
                foundInfo = True
            elif lines[ii].strip("\n") == "      \"infoHotspots\": []":
                foundInfo = True
                foundAllInfo = True
            elif lines[ii].startswith("      \"initialViewParameters\""):
                if lines[ii+1].startswith("        \"yaw\": "):
                    initYaw = float((lines[ii+1].removeprefix("        \"yaw\": ")).removesuffix(",\n"))
                    ii += 2
                elif lines[ii+1].startswith("        \"pitch\": "):
                    initYaw = float((lines[ii+2].removeprefix("        \"yaw\": ")).removesuffix(",\n"))
                    ii += 3
            else:
                ii += 1

        hotspots = []
        infoTitles = []
        # Loop through info hotspots if there are any
        while not foundAllInfo:
            if lines[ii].strip("\n") == "    }," or lines[ii].strip('\n') == "    }":
                foundAllInfo = True
            elif lines[ii].startswith("          \"yaw\": "):
                yaw = float((lines[ii].removeprefix("          \"yaw\": ")).removesuffix(",\n"))
                pitch = float((lines[ii+1].removeprefix("          \"pitch\": ")).removesuffix(",\n"))
                title = (lines[ii+2].removeprefix("          \"title\": \"")).removesuffix("\",\n")
                text = (lines[ii+3].removeprefix("          \"text\": \"")).removesuffix("\"\n")

                hotspots.append(InfoHotspot(initYaw, yaw, pitch, title, text))
                infoTitles.append(title)
                ii += 4
            else:
                ii += 1
        return (hotspots, infoTitles, initYaw)

# Imports a list of link hotspots for a given image, and uses these to update the data.js file at the given filepath
def implementLinkChanges(mainDir, imageID, hsList):
    with open(mainDir + "/app-files/data.js", 'r') as fr:
        lines = fr.readlines()

        with open(mainDir + "/app-files/data.js.txt", 'w+') as fw:
            atEditImage = False
            atLinkList = False
            ii = 0 # Iterator Variable

            # Find correct data entry and start of hotspots of this entry
            while not atLinkList and ii < len(lines):
                if atEditImage and (lines[ii].strip('\n') == "      \"linkHotspots\": [" or lines[ii].strip('\n') == "      \"linkHotspots\": [],"):
                    atLinkList = True
                elif lines[ii].strip('\n') == f"      \"id\": \"{imageID}\",":
                    atEditImage = True # Allows first condition of if/else block to be true now that correct data entry is being searched
                    fw.write(lines[ii])
                else:
                    fw.write(lines[ii])
                ii += 1

            if len(hsList) == 0: # No links for given image
                fw.write("      \"linkHotspots\": [],\n")
            else: # Write all hotspots in given list to data.js file
                fw.write("      \"linkHotspots\": [\n")
                hotspotsWritten = 0
                for hs in hsList:
                    fw.write(hs.toString())
                    hotspotsWritten += 1
                    if hotspotsWritten < len(hsList):
                        fw.write(',')
                    fw.write('\n')
                fw.write("      ],\n")

            # Print remaining data back into file
            pastRelevantData = False
            while ii < len(lines):
                if pastRelevantData:
                    fw.write(lines[ii])
                elif lines[ii].startswith("      \"infoHotspots\""):
                    pastRelevantData = True
                    fw.write(lines[ii])
                ii += 1

    os.remove(mainDir + "/app-files/data.js") # Remove the original file
    os.rename(mainDir + "/app-files/data.js.txt", mainDir + "/app-files/data.js") # Change the name of the new/updated file to the original file's name

# Imports a list of info hotspots for a given image, and uses these to update the data.js file at the given filepath
def implementInfoChanges():
    print('yeh ok')

# Using the given parameters, will create a new Link Hotspot, and add it to the list
def addLinkHotspot(hsList, idList, newYaw, newPitch, newTarget, initYaw):
    newHS = LinkHotspot(initYaw, 0, 0, newTarget) # Enter pitch and yaw as 0, add them separately using their setters which convert degrees --> radians
    newHS.setTruePitch(newPitch)
    newHS.setTrueYaw(newYaw)
    hsList.append(newHS)
    idList.append(newHS.getTarget())
    return (copyHotspotList(hsList, 'Link'), copyIDList(idList))

# Updates the parameters of a pre-existing link hotspot based on given values
def editLinkHotspot(hsList, updIdx, newYaw, newPitch, newTarget):
    newHSList = copyHotspotList(hsList, 'Link')
    newHSList[updIdx].setTruePitch(newPitch)
    newHSList[updIdx].setTrueYaw(newYaw)
    newHSList[updIdx].setTarget(newTarget)
    return newHSList

# Using the given parameters, will create a new Info Hotspot, and add it to the list
def addInfoHotspot(hsList, idList, newYaw, newPitch, newTitle, newText, initYaw):
    title = newTitle.replace('\n','<br>') # Replace newline characters with more HTML friendly code
    text = newText.replace('\n','<br>')
    newHS = InfoHotspot(initYaw, 0, 0, title, text) # Enter pitch and yaw as 0, add them separately using their setters which convert degrees --> radians
    newHS.setTruePitch(newPitch)
    newHS.setTrueYaw(newYaw)
    hsList.append(newHS)
    idList.append(newHS.getTitle())
    return (copyHotspotList(hsList, 'Info'), copyIDList(idList))

# Updates the parameters of a pre-existing info hotspot based on given values
def editInfoHotspot(hsList, updIdx, newYaw, newPitch, newTitle, newText):
    title = newTitle.replace('\n','<br>') # Replace newline characters with more HTML friendly code
    text = newText.replace('\n','<br>')
    newHSList = copyHotspotList(hsList, 'Info')
    newHSList[updIdx].setTruePitch(newPitch)
    newHSList[updIdx].setTrueYaw(newYaw)
    if not newTitle == '': # If there was an input to the box, change hotspot title
        newHSList[updIdx].setTitle(title)
    if not newText == '': # If there was an input to the box, change hotspot text
        newHSList[updIdx].setText(text)
    return newHSList

# Remove the specified hotspot from the list and ID list
def deleteHotspot(hotspotList, hotspotIDList, selHotspotID, hsType):
    idxNum = int((selHotspotID.split(':'))[0])
    hotspotList.pop(idxNum)
    hotspotIDList.pop(idxNum)
    return (copyHotspotList(hotspotList, hsType), copyIDList(hotspotIDList))

# Makes a copy of the list of Hotspots used in modifying image hotspots
def copyHotspotList(hsList, hsType):
    newList = []
    for hs in hsList:
        if hsType == 'Link':
            newList.append(LinkHotspot(hs.getInitYaw(),hs.getTrueYaw(),hs.getTruePitch(),hs.getTarget()))
        elif hsType == 'Info':
            newList.append(InfoHotspot(hs.getInitYaw(),hs.getTrueYaw(),hs.getTruePitch(),hs.getTitle(),hs.getText()))
    return newList

# Makes a copy of the list of IDs used in modifying image hotspots
def copyIDList(idList):
    newList = []
    for id in idList:
        newList.append(id)
    return newList