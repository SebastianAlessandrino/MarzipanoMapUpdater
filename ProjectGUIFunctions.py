# File: ProjectGUIFunctions.py
# By: Sebastian Alessandrino
# Date Created: 29/01/2022
# Purpose: Supporting functions for facilitating parts of the GUI and validating input fields

import PySimpleGUI as sg
from os import path
import os
import UpdateHotspotFunctions as uhf
from Hotspot import Hotspot # For using validation functions
import pandas as pd

# Produces a window that prompts the user to input the folder of the main tour to be edited or updated by the rest of the program
# The code will loop until a valid tour file is provided
def selectMainDirMenu():
    selectMainDirLayout = [ [sg.Text('Select Tour (Main Folder) to Edit or Update:')],
                            [sg.Text('Tour Folder:', size=(10,1)), sg.InputText(), sg.FolderBrowse()],
                            [sg.Button('Continue', key='continue')]]

    # Main Tour Selection
    mainDirPath = "" # Failsafe for if the exit button is pressed
    mainDirName = "" # Failsafe for if the exit button is pressed
    selectMainDirActive = True
    continueProgram = True # Used to determine whether to skip further menus
    selectMainDir = sg.Window('Select Main Tour', selectMainDirLayout)
    while selectMainDirActive and continueProgram:
        event, values = selectMainDir.read() # Will only read values as None if using exit button
        if event == sg.WIN_CLOSED: # Check if window closed
            continueProgram = False
        if event == 'continue' and continueProgram: # Skip if closed
            if not values == None:
                validDir, errMsg, mainDirName = validateMainDir(values[0], tourType='m')
                if validDir:
                    mainDirPath = values[0]
                    selectMainDirActive = False
                else:
                    errorPopup(errMsg)
    selectMainDir.close()
    return (mainDirPath, mainDirName, continueProgram)

# The window that acts as the main menu for the program
# It will allow the user to update the main map file, edit/add a link, edit/add a hotspot or exit
def mainMenu(tourName):
    mainMenuLayout = [  [sg.Text(f'Choose a Function for Tour: \'{tourName}\'')],
                        [sg.Button('Update Tour', key='update', size=(25,1)), sg.Button('Update Tour Menu', key='menu', size=(25,1))],
                        [sg.Button('Edit Image Links', key='link', size=(25,1)), sg.Button('Edit Image Info', key='info', size=(25,1))],
                        [sg.Button('Exit', key='exit', size=(25,1))]]

    selection = "exit" # Selection is set to exit by default
    mainMenuActive = True
    continueProgram = True
    mainMenuWindow = sg.Window('Main Menu', mainMenuLayout, element_justification='c')
    while mainMenuActive and continueProgram:
        event, _ = mainMenuWindow.read()
        if event == sg.WIN_CLOSED or event == 'exit':
            continueProgram = False
        elif event == 'update' or event == 'link' or event == 'info' or event == 'menu':
            selection = event
            mainMenuActive = False
    mainMenuWindow.close()
    return (selection, continueProgram)

# Will prompt the user to input paths to the supporting data (Image List and Update Directory)
# Will utilise validation functions to ensure that inputs are correct
def selectSupportDataMenu(mainDirPath):
    supMenuLayout = [   [sg.Text('Select Image List (CSV File) and Update Tour (Main Folder):')],
                        [sg.Text('List File:  ', size=(10,1)), sg.InputText(), sg.FileBrowse()],
                        [sg.Text('Tour Folder:', size=(10,1)), sg.InputText(), sg.FolderBrowse()],
                        [sg.Button('Continue', key='continue', size=(25,1)), sg.Button('Go Back', key='back', size=(25,1))]]

    updateDirPath = ""
    updateDirName = ""
    listPath = ""
    listName = ""
    supMenuActive = True
    continueProgram = True
    returnToMainMenu = False
    selectSupData = sg.Window('Update Data Selection', supMenuLayout)
    while supMenuActive and continueProgram:
        event, values = selectSupData.read() # Will only read values as None if using exit button
        if event == sg.WIN_CLOSED: # Check if window closed
            continueProgram = False
        if event == 'back' and continueProgram:
            supMenuActive = False
            returnToMainMenu = True
        elif event == 'continue' and continueProgram: # Skip if closed
            if not values == None:
                validList, listErrMsg, listName = validateList(values[0])
                validDir, dirErrMsg, updateDirName = validateMainDir(values[1])

                if values[1] == mainDirPath: # If the main and update paths are the same, invalid
                    validDir = False
                    dirErrMsg = 'The Update Directory must not be the same as the Main Tour to be updated!'
                    # Can override the error message from before since if the paths are the same, the directory must be valid since the main dir is valid

                if validDir and validList: # If both are valid then assign values and exit loop
                    listPath = values[0]
                    updateDirPath = values[1]
                    supMenuActive = False
                if not validList: # Error case for invalid list given
                    errorPopup(listErrMsg)
                if not validDir: # Error case for invalid update tour given
                    errorPopup(dirErrMsg)
    selectSupData.close() # Close window if exitting loop
    return (updateDirPath, updateDirName, listPath, listName, continueProgram, returnToMainMenu)

# Will make the user input an image list, to be used for exclusively updating the tour menu
def selectImageListMenu():
    imgMenuLayout = [   [sg.Text('Select Image List (CSV File) and Update Tour (Main Folder):')],
                        [sg.Text('List File:  ', size=(10,1)), sg.InputText(), sg.FileBrowse()],
                        [sg.Button('Continue', key='continue', size=(25,1)), sg.Button('Go Back', key='back', size=(25,1))]]

    listPath = ""
    listName = ""
    imgMenuActive = True
    continueProgram = True
    returnToMainMenu = False
    selectImgData = sg.Window('Update List Selection', imgMenuLayout)
    while imgMenuActive and continueProgram:
        event, values = selectImgData.read() # Will only read values as None if using exit button
        if event == sg.WIN_CLOSED: # Check if window closed
            continueProgram = False
        if event == 'back' and continueProgram:
            imgMenuActive = False
            returnToMainMenu = True
        elif event == 'continue' and continueProgram: # Skip if closed
            if not values == None:
                validList, listErrMsg, listName = validateList(values[0])
                if validList: # If the list is valid, assign value and exit loop
                    listPath = values[0]
                    imgMenuActive = False
                if not validList: # Error case for invalid list given
                    errorPopup(listErrMsg)
    selectImgData.close() # Close window if exitting loop
    return (listPath, listName, continueProgram, returnToMainMenu)

# Used for selecting from a list box, generally for selecting an image or hotspot
def selectFromListMenu(title, text, imgList):
    layout = [  [sg.Text(text)],
                [sg.Listbox(values=imgList, size=(60,10))],
                [sg.Button('Continue', key='continue', size=(25,1)), sg.Button('Go Back', key='back', size=(25,1))]]

    selection = ""
    listMenuActive = True
    continueProgram = True
    returnToMainMenu = False
    listMenu = sg.Window(title, layout)
    while listMenuActive and continueProgram:
        event, values = listMenu.read()
        if event == sg.WIN_CLOSED:
            continueProgram = False
        if event == 'back' and continueProgram:
            listMenuActive = False
            returnToMainMenu = True
        elif event == 'continue' and continueProgram: # Skip if closed
            if not len(values[0]) == 0:
                selection = values[0][0] # Value for reading listbox is given as a list rather than a single value
                listMenuActive = False
            else:
                errorPopup("An image must be selected!")
    listMenu.close()
    return (selection, continueProgram, returnToMainMenu)

# Lets the user select a function for the hotspots of a selected image
def hotspotMenu(selectedImage, IDList, changesUnsaved, hsType):
    labelledList = labelIDList(IDList)
    hotspotMenuLayout = [   [sg.Text(f'Add a hotspot or else choose one to edit or delete below:')],
                            [sg.Listbox(values=labelledList, size=(60,10))],
                            [sg.Button('Add', key='add', size=(25,1)), sg.Button('Edit', key='edit', size=(25,1))],
                            [sg.Button('Delete', key='del', size=(25,1)), sg.Button('Save Changes', key='save', size=(25,1))],
                            [sg.Button('Go Back', key='back', size=(25,1))]]

    if changesUnsaved:
        hotspotMenuLayout.append([sg.Text('NOTE: There are currently unsaved changes!')])

    selection = "back" # Selection is set to go back by default
    hotspotName = ""
    menuActive = True
    continueProgram = True
    continueHotspots = True
    hotspotMenuWindow = sg.Window(f'{hsType} Hotspot Menu (Image: \'{selectedImage}\')', hotspotMenuLayout, element_justification='c')
    while menuActive and continueProgram and continueHotspots:
        event, values = hotspotMenuWindow.read()
        if event == sg.WIN_CLOSED:
            continueProgram = False
        elif event == 'back':
            continueHotspots = False
        elif event == 'add' or event == 'save':
            selection = event
            menuActive = False
        elif event == 'edit' or event == 'del':
            if not len(values[0]) == 0:
                selection = event
                hotspotName = values[0][0]
                menuActive = False
            else:
                errorPopup("A hotspot must be selected for this action!")
    hotspotMenuWindow.close()
    return (selection, hotspotName, continueProgram, continueHotspots)

# Function for providing the menu necessary to add a new link hotspot to a selected image
def addLinkHotspotMenu(hotspotList, idList, imgList, initYaw, unsavedChanges):
    addLHSMenuLayout = [    [sg.Text('Input parameters for new Link Hotspot:')],
                            [sg.Text('Yaw must be in degrees and >-180 and <=180, where +ve yaw is right and -ve is left.')],
                            [sg.Text('Pitch must be in degrees and >-90 and <=90 where +ve pitch is down and -ve is up.')],
                            [sg.Text('YAW:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('PITCH:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('TARGET:', size=(10,1))],
                            [sg.Listbox(values=imgList, size=(60,10))],
                            [sg.Button('Add Hotspot', key='add', size=(25,1)), sg.Button('Cancel', key='cancel', size=(25,1))]]

    newList = uhf.copyHotspotList(hotspotList, 'Link') # Make a copy in case popup is exitted without change
    newIDList = uhf.copyIDList(idList)
    menuActive = True
    addLHSMenu = sg.Window('Add New Link Hotspot', addLHSMenuLayout)
    while menuActive:
        yawValid = True
        pitchValid = True # Assume valid inputs
        event, values = addLHSMenu.read()
        if event == sg.WIN_CLOSED or event == 'cancel': # Check if window closed or cancel button pressed
            menuActive = False
        if event == 'add':
            if not values[0] == '' and not values[1] == '' and not len(values[2]) == 0:
                try: # Ensure a number is entered for yaw
                    yaw = float(values[0])
                except:
                    yawValid = False
                    errorPopup("Input for yaw must be a number!")

                try: # Ensure a number is entered for pitch
                    pitch = float(values[1])
                except:
                    pitchValid = False
                    errorPopup("Input for pitch must be a number!")

                if yawValid and not Hotspot.validateYawDegrees(None, yaw): # Ensure entered value is within correct bounds
                    yawValid = False
                    errorPopup("Input yaw is not in valid range!")
                if pitchValid and not Hotspot.validatePitchDegrees(None, pitch): # Ensure entered value is within correct bounds
                    pitchValid = False
                    errorPopup("Input pitch is not in valid range!")

                if yawValid and pitchValid: # If no issues, add the new link
                    newList, newIDList = uhf.addLinkHotspot(hotspotList, idList, yaw, pitch, values[2][0], initYaw)
                    unsavedChanges = True
                    menuActive = False
            else:
                errorPopup("Some fields are not filled!")
    addLHSMenu.close() # Close window if exitting loop
    return (newList, newIDList, unsavedChanges)

# Function for providing the menu necessary to edit an existing link hotspot of a selected image
def editLinkHotspotMenu(hotspotList, hotspotIDList, chosenHS, imgList, unsavedChanges):
    chosenHSIdx = int((chosenHS.split(':'))[0])
    curYaw = '{:.2f}'.format(hotspotList[chosenHSIdx].getRelativeYawDegrees()) # Given as a string
    curPit = '{:.2f}'.format(hotspotList[chosenHSIdx].getTruePitchDegrees()) # Given as a string
    curTar = hotspotList[chosenHSIdx].getTarget()
    edtLHSMenuLayout = [    [sg.Text('Current parameters of selected Link Hotspot:')],
                            [sg.Text(f'YAW: {curYaw}{chr(176)}', size=(10,1)), sg.Text(f'PITCH: {curPit}{chr(176)}', size=(10,1))],
                            [sg.Text(f'TARGET: {curTar}')],
                            [sg.Text('')],
                            [sg.Text('New yaw must be in degrees and >-180 and <=180, where +ve yaw is right and -ve is left.')],
                            [sg.Text('New pitch must be in degrees and >-90 and <=90 where +ve pitch is down and -ve is up.')],
                            [sg.Text('NEW YAW:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('NEW PITCH:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('NEW TARGET:')],
                            [sg.Listbox(values=imgList, size=(60,10))],
                            [sg.Button('Update Hotspot', key='edt', size=(25,1)), sg.Button('Cancel', key='cancel', size=(25,1))]]

    newList = uhf.copyHotspotList(hotspotList, 'Link') # Make a copy in case popup is exitted without change
    newIDList = uhf.copyIDList(hotspotIDList)
    menuActive = True
    edtLHSMenu = sg.Window('Edit Existing Link Hotspot', edtLHSMenuLayout)
    while menuActive:
        yawValid = True
        pitchValid = True # Assume valid inputs
        event, values = edtLHSMenu.read()
        if event == sg.WIN_CLOSED or event == 'cancel': # Check if window closed or cancel button pressed
            menuActive = False
        if event == 'edt':
            if not values[0] == '' and not values[1] == '' and not len(values[2]) == 0:
                try: # Ensure a number is entered for yaw
                    yaw = float(values[0])
                except:
                    yawValid = False
                    errorPopup("Input for new yaw must be a number!")

                try: # Ensure a number is entered for pitch
                    pitch = float(values[1])
                except:
                    pitchValid = False
                    errorPopup("Input for new pitch must be a number!")

                if yawValid and not Hotspot.validateYawDegrees(None, yaw): # Ensure entered value is within correct bounds
                    yawValid = False
                    errorPopup("Input yaw is not in valid range!")
                if pitchValid and not Hotspot.validatePitchDegrees(None, pitch): # Ensure entered value is within correct bounds
                    pitchValid = False
                    errorPopup("Input pitch is not in valid range!")

                if yawValid and pitchValid: # If no issues, edit the existing link
                    newList = uhf.editLinkHotspot(hotspotList, chosenHSIdx, yaw, pitch, values[2][0])
                    newIDList[chosenHSIdx] = newList[chosenHSIdx].getTarget()
                    unsavedChanges = True
                    menuActive = False
            else:
                errorPopup("Some fields are not filled!")
    edtLHSMenu.close() # Close window if exitting loop
    return (newList, newIDList, unsavedChanges)

# Function for providing the menu necessary to add a new info hotspot to a selected image
def addInfoHotspotMenu(hotspotList, idList, initYaw, unsavedChanges):
    addIHSMenuLayout = [    [sg.Text('Input parameters for new Info Hotspot:')],
                            [sg.Text('Yaw must be in degrees and >-180 and <=180, where +ve yaw is right and -ve is left.')],
                            [sg.Text('Pitch must be in degrees and >-90 and <=90 where +ve pitch is down and -ve is up.')],
                            [sg.Text('YAW:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('PITCH:', size=(10,1)), sg.InputText(size=(45,1))],
                            [sg.Text('NOTE: Long inputs for title may not be shown in the actual display given it only shows the first 2 lines.')],
                            [sg.Text('NOTE: Furthermore, a longer line may also cause the second line to also not be displayed.')],
                            [sg.Text('TITLE:', size=(10,1))], [sg.Multiline(size=(60,2))],
                            [sg.Text('TEXT:', size=(10,1))], [sg.Multiline(size=(60,5))],
                            [sg.Button('Add Hotspot', key='add', size=(25,1)), sg.Button('Cancel', key='cancel', size=(25,1))]]

    newList = uhf.copyHotspotList(hotspotList, 'Info') # Make a copy in case popup is exitted without change
    newIDList = uhf.copyIDList(idList)
    menuActive = True
    addIHSMenu = sg.Window('Add New Info Hotspot', addIHSMenuLayout)
    while menuActive:
        yawValid = True
        pitchValid = True # Assume valid inputs
        event, values = addIHSMenu.read()
        if event == sg.WIN_CLOSED or event == 'cancel': # Check if window closed or cancel button pressed
            menuActive = False
        if event == 'add':
            if not values[0] == '' and not values[1] == '': # No error checking for title or text, given they can be essentially any string
                try: # Ensure a number is entered for yaw
                    yaw = float(values[0])
                except:
                    yawValid = False
                    errorPopup("Input for yaw must be a number!")

                try: # Ensure a number is entered for pitch
                    pitch = float(values[1])
                except:
                    pitchValid = False
                    errorPopup("Input for pitch must be a number!")

                if yawValid and not Hotspot.validateYawDegrees(None, yaw): # Ensure entered value is within correct bounds
                    yawValid = False
                    errorPopup("Input yaw is not in valid range!")
                if pitchValid and not Hotspot.validatePitchDegrees(None, pitch): # Ensure entered value is within correct bounds
                    pitchValid = False
                    errorPopup("Input pitch is not in valid range!")

                if yawValid and pitchValid: # If no issues, add the new link
                    newList, newIDList = uhf.addInfoHotspot(hotspotList, idList, yaw, pitch, values[2], values[3], initYaw)
                    unsavedChanges = True
                    menuActive = False
            else:
                errorPopup("Some fields (yaw or pitch) are not filled!")
    addIHSMenu.close() # Close window if exitting loop
    return (newList, newIDList, unsavedChanges)

# Function for providing the menu necessary to edit an existing info hotspot of a selected image
def editInfoHotspotMenu(hotspotList, hotspotIDList, chosenHS, unsavedChanges):
    chosenHSIdx = int((chosenHS.split(':'))[0])
    curYaw = '{:.2f}'.format(hotspotList[chosenHSIdx].getRelativeYawDegrees()) # Given as a string
    curPit = '{:.2f}'.format(hotspotList[chosenHSIdx].getTruePitchDegrees()) # Given as a string
    curTit = hotspotList[chosenHSIdx].getTitle()
    curTex = hotspotList[chosenHSIdx].getText()
    edtIHSMenuLayout = formIHSEditLayout(curYaw, curPit, curTit, curTex)

    newList = uhf.copyHotspotList(hotspotList, 'Info') # Make a copy in case popup is exitted without change
    newIDList = uhf.copyIDList(hotspotIDList)
    menuActive = True
    edtIHSMenu = sg.Window('Edit Existing Info Hotspot', edtIHSMenuLayout)
    while menuActive:
        yawValid = True
        pitchValid = True # Assume valid inputs
        event, values = edtIHSMenu.read()
        if event == sg.WIN_CLOSED or event == 'cancel': # Check if window closed or cancel button pressed
            menuActive = False
        if event == 'edt':
            if not values[0] == '' and not values[1] == '': # No error checking for title or text, given they can be essentially any string
                try: # Ensure a number is entered for yaw
                    yaw = float(values[0])
                except:
                    yawValid = False
                    errorPopup("Input for new yaw must be a number!")

                try: # Ensure a number is entered for pitch
                    pitch = float(values[1])
                except:
                    pitchValid = False
                    errorPopup("Input for new pitch must be a number!")

                if yawValid and not Hotspot.validateYawDegrees(None, yaw): # Ensure entered value is within correct bounds
                    yawValid = False
                    errorPopup("Input yaw is not in valid range!")
                if pitchValid and not Hotspot.validatePitchDegrees(None, pitch): # Ensure entered value is within correct bounds
                    pitchValid = False
                    errorPopup("Input pitch is not in valid range!")

                if yawValid and pitchValid: # If no issues, edit the existing link
                    newList = uhf.editInfoHotspot(hotspotList, chosenHSIdx, yaw, pitch, values[2], values[3])
                    newIDList[chosenHSIdx] = newList[chosenHSIdx].getTitle()
                    unsavedChanges = True
                    menuActive = False
            else:
                errorPopup("Some fields (yaw or pitch) are not filled!")
    edtIHSMenu.close() # Close window if exitting loop
    return (newList, newIDList, unsavedChanges)

# Asks the user to verify that they want to delete the selected hotspot
def deleteHotspotPopup(hotspotList, idList, hotspotName, imageName, hsType, unsavedChanges):
    delPopLayout = [    [sg.Text(f'Delete {hsType} Hotspot \'{hotspotName}\' from Image \'{imageName}\'?')],
                        [sg.Button('Yes',key='y',size=(10,1)), sg.Button('No',key='n',size=(10,1))]]

    newList = uhf.copyHotspotList(hotspotList, hsType) # Make a copy in case popup is exitted without change
    newIDList = uhf.copyIDList(idList)
    delPop = sg.Window('Continue?', delPopLayout, element_justification='c')
    popupActive = True
    while popupActive:
        event, _ = delPop.read()
        if event == sg.WIN_CLOSED or event == 'n':
            popupActive = False
        elif event == 'y':
            newList, newIDList = uhf.deleteHotspot(hotspotList, idList, hotspotName, hsType)
            unsavedChanges = True
            popupActive = False
    delPop.close()
    return (newList, newIDList, unsavedChanges)

# Creates a window asking if the user wants to save their changes
# To be used when exitting program or 'Going Back' without saving
def saveChangesPopup():
    savPopLayout = [    [sg.Text(f'There are unsaved changes to hotspots, do you wish to save?')],
                        [sg.Text('Note: Pressing the X button will not save changes.')],
                        [sg.Button('Yes',key='y',size=(10,1)), sg.Button('No',key='n',size=(10,1))]]

    output = 'y' # Assume yes
    savPop = sg.Window('Save Changes?', savPopLayout, element_justification='c')
    popupActive = True
    while popupActive:
        event, _ = savPop.read()
        if event == sg.WIN_CLOSED or event == 'n':
            popupActive = False
            output = 'n'
        elif event == 'y':
            popupActive = False
    savPop.close()
    return output

# Will open a window with a specified error message
def errorPopup(errMsg):
    errorMenuLayout = [ [sg.Text('ERROR:')],
                        [sg.Text(errMsg)],
                        [sg.Button('OK',key='ok',size=(10,1))]]

    errPop = sg.Window('ERROR', errorMenuLayout, modal=True, element_justification='c')
    while True:
        event, _ = errPop.read()
        if event == sg.WIN_CLOSED or event == 'ok':
            break
    errPop.close()

# Returns a window layout that tells the user that the tour file is being updated such that they do not close the program
# whilst this is occurring
def updateTourPopup(mainTourPath, listFilePath, updTourPath):
    popupLayout = [ [sg.Text('THE PROGRAM IS ABOUT TO BEGIN AN UPDATE USING THE FOLLOWING DATA:')],
                    [sg.Text('Selected Tour:', size=(10,1)), sg.Text(f'{mainTourPath}')],
                    [sg.Text('List File:', size=(10,1)), sg.Text(f'{listFilePath}')],
                    [sg.Text('Update Tour:', size=(10,1)), sg.Text(f'{updTourPath}')],
                    [sg.Text('')],
                    [sg.Text('DO NOT CLOSE THE PROGRAM WHILST THIS IS OCCURRING!!!')],
                    [sg.Text('DOING SO MAY CAUSE SEVERE DAMAGE TO THE TOUR FILE!!!')],
                    [sg.Text('')],
                    [sg.Text('Press \'OK\' or close this popup to commence the update...')],
                    [sg.Button('OK',key='ok',size=(10,1)), sg.Button('Cancel',key='cancel',size=(10,1))]]

    continueUpdate = True
    popup = sg.Window('IMPORTANT: About to Update', popupLayout)
    while True:
        event, _ = popup.read()
        if event == sg.WIN_CLOSED or event == 'ok':
            break
        elif event == 'cancel':
            continueUpdate = False
            break

    popup.close()
    return continueUpdate

# Opens a window with a message indicating the name and location of the logfile produced during the update
def updateCompletePopup(mainTourPath, listFilePath, updTourPath, logfile, errors):
    updPopupLayout = [  [sg.Text('PROCESS SUMMARY')],
                        [sg.Text('Selected Tour:', size=(10,1)), sg.Text(f'{mainTourPath}')],
                        [sg.Text('List File:', size=(10,1)), sg.Text(f'{listFilePath}')],
                        [sg.Text('Update Tour:', size=(10,1)), sg.Text(f'{updTourPath}')],
                        [sg.Text('')],
                        [sg.Text('LogFile Path:', size=(10,1)), sg.Text(f'{logfile}')],
                        [sg.Text('Total Errors:', size=(10,1)), sg.Text(f'{errors}')],
                        [sg.Button('OK',key='ok',size=(10,1))]]

    updPop = sg.Window('Update Completed', updPopupLayout)
    while True:
        event, _ = updPop.read()
        if event == sg.WIN_CLOSED or event == 'ok':
            break
    updPop.close()

# Will check the provided path and ensure that it is valid
# To be valid, it must be a directory and contain a folder called 'app-files' which then contains the following files/directories:
# /tiles (expected to have at least one folder in it) and data.js
# If the directory is a main tour file it must also include 
def validateMainDir(dirPath, tourType = 'u'):
    outputStr = ""
    valid = False
    dirPathParts = dirPath.split('/')
    dirName = dirPathParts[len(dirPathParts) - 1] # Get last element of path, will be the dirName if it is a directory otherwise will not be used
    if not dirPath == "":
        if path.isdir(dirPath):
            if path.isdir(dirPath + '/app-files/tiles'):
                if len(os.listdir(dirPath + '/app-files/tiles')) > 0:
                    if path.isfile(dirPath + '/app-files/data.js'):
                        if tourType == 'u' or (tourType == 'm' and path.isfile(dirPath + '/app-files/index.html') and path.isfile(dirPath + '/app-files/index.js')): 
                            valid = True # ^^^ Update Directory OR Main Directory AND index.html AND index.js Exists
                        else:
                            outputStr = f"Folder '.../{dirName}/app-files' must contain both an index.js and index.html file!"
                    else:
                        outputStr = f"Folder '.../{dirName}/app-files' does not contain a data.js file!"
                else:
                    outputStr = f"Folder '.../{dirName}/app-files/tiles' does not contain any image/tile folders!"
            else:
                outputStr = f"Folder '.../{dirName}/app-files/tiles' was not found. Folder containing images/tiles is required!"
        else:
            outputStr = "Main tour folder must be provided for given tour!"
    else:
        outputStr = "No tour folder provided!"

    return (valid, outputStr, dirName)

# Will check the provided path to ensure it leads to a valid .csv file
# To be valid, it must be of the correct type
# Correct form of the excel file will be provided on an accompanying wiki page
def validateList(filePath):
    outputStr = ""
    valid = False
    filePathParts = filePath.split('/')
    fileName = filePathParts[len(filePathParts)-1]
    if not filePath == "":
        if path.isfile(filePath):
            if fileName.endswith('.xlsx') or fileName.endswith('.xls'):
                data = pd.read_excel(filePath, keep_default_na=False) # Ensure file header is valid, therefore file is assumed valid
                hdrs = data.columns.values.tolist()
                if hdrs[0] == 'Num.' and hdrs[1] == 'Name' and hdrs[2] == 'ID' and hdrs[3] == 'Include in Menu' and hdrs[4] == 'Comment':
                    valid = True
                else:
                    outputStr = f"Ensure given file is an Image List file with the appropriate headers! See Wiki for Details!"
            else:
                outputStr = f"Provided file '{fileName}' is not an Excel file (.xlsx or .xls)!"
        else:
            outputStr = "Provided path is not an Excel spreadsheet file!"
    else:
        outputStr = "No list file provided!"

    return (valid, outputStr, fileName)

# Lists the folders in the Main Tour Folder's 'tiles' directory
# These correspond to images currently within the project
def listTourImages(tourDir):
    return os.listdir(tourDir + "/app-files/tiles/")

# Will add an identifier to the beginning of a list of hotspot IDs given that
# differentiation between those with the same names may be required
def labelIDList(idList):
    labelledList = []
    ii = 0
    for id in idList:
        labelledList.append(str(ii) + ':' + id)
        ii += 1
    return labelledList

# Creates a list in the form of a window layout to be used for editting Info Hotspots
def formIHSEditLayout(yaw, pitch, title, text):
    titleList = title.split('<br>')
    textList = text.split('<br>')

    layout = [  [sg.Text('Current parameters of selected Info Hotspot:')],
                [sg.Text(f'YAW:', size=(10,1)), sg.Text(f'PITCH:', size=(10,1))],
                [sg.Text(f'{yaw}{chr(176)}', size=(10,1)), sg.Text(f'{pitch}{chr(176)}', size=(10,1))],
                [sg.Text('')]]

    # Add title display to layout
    linesAdded = 0
    layout.append([sg.Text('TITLE:')])
    while linesAdded < 2 and linesAdded < len(titleList):
        layout.append([sg.Text(titleList[linesAdded], size=(60,1))])
        linesAdded += 1

    if len(titleList) > 2: # Show that some lines are omitted to save space
        layout.append([sg.Text('...')])

    # Add text display to layout
    linesAdded = 0
    layout.extend([[sg.Text('')], [sg.Text('TEXT:')]])
    while linesAdded < 5 and linesAdded < len(textList):
        layout.append([sg.Text(textList[linesAdded], size=(60,1))])
        linesAdded += 1

    if len(textList) > 5: # Show that some lines are omitted to save space
        layout.append([sg.Text('...')])
    
    layout.extend([ [sg.Text('')],
                    [sg.Text('New yaw must be in degrees and >-180 and <=180, where +ve yaw is right and -ve is left.')],
                    [sg.Text('New pitch must be in degrees and >-90 and <=90 where +ve pitch is down and -ve is up.')],
                    [sg.Text('NEW YAW:', size=(10,1)), sg.InputText(size=(45,1))],
                    [sg.Text('NEW PITCH:', size=(10,1)), sg.InputText(size=(45,1))],
                    [sg.Text('NOTE: Long inputs for title may not be shown in the actual display given it only shows the first 2 lines.')],
                    [sg.Text('NOTE: Furthermore, a longer line may also cause the second line to also not be displayed.')],
                    [sg.Text('NOTE: If Title or Text inputs are left blank, no change will be made.')],
                    [sg.Text('NEW TITLE:', size=(10,1))], [sg.Multiline(size=(60,2))],
                    [sg.Text('NEW TEXT:', size=(10,1))], [sg.Multiline(size=(60,5))],
                    [sg.Button('Update Hotspot', key='edt', size=(25,1)), sg.Button('Cancel', key='cancel', size=(25,1))]])
    return layout