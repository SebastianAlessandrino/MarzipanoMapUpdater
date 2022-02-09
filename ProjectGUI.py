# File: ProjectGUI.py
# By: Sebastian Alessandrino
# Date Created: 29/01/2022
# Purpose: The main program for running the GUI to update the Map Project or data of said project

import PySimpleGUI as sg
import ProjectGUIFunctions as pgf
import UpdateMap as um
import UpdateHotspotFunctions as uhf
from InfoHotspot import InfoHotspot
from LinkHotspot import LinkHotspot

sg.theme('SystemDefault')

mainDirPath, mainDirName, continueProgram = pgf.selectMainDirMenu()

while continueProgram: # Continue if valid main tour directory entered and exit button not clicked
    selection, continueProgram = pgf.mainMenu(mainDirName)

    if selection == 'update' and continueProgram: # Prompts user to update file and lets them select a list file and update directory
        updDirPath, updDirName, listPath, listName, continueProgram, goBack = pgf.selectSupportDataMenu()

        if continueProgram and not goBack: # Continue if valid files/directories are given and the exit button is not clicked
            logfileName, errors = um.performMapUpdate(mainDirPath, listPath, updDirPath, mainDirName)
            pgf.updateCompletePopup(mainDirPath, listPath, updDirPath, logfileName, errors)
            # Update process complete, go back to function selection menu
    elif selection == 'menu' and continueProgram: # Prompts user to update menu of file and lets them select a list file
        listPath, listName, continueProgram, goBack = pgf.selectImageListMenu()

        if continueProgram and not goBack: # Continue if valid list file is provided
            logfileName = um.performMenuUpdate(listPath, mainDirPath, mainDirName, '', True)
            pgf.updateCompletePopup(mainDirPath, listPath, 'N/A', logfileName, 'N/A')
    elif selection == 'link' and continueProgram:
        imageList = pgf.listTourImages(mainDirPath)
        imageSelected, continueProgram, goBack = pgf.selectFromListMenu('Edit Link Hotspots', 'Select Image Data to Edit:', imageList)

        changesUnsaved = False
        continueHotspots = True
        if continueProgram and not goBack:
            hotspotList, hotspotIDList, initYaw = uhf.listLinkHotspots(mainDirPath, imageSelected)
        while continueProgram and continueHotspots and not goBack: # If image appropriately selected
            sel2, modifiedHotspotID, continueProgram, continueHotspots = pgf.hotspotMenu(imageSelected, hotspotIDList, changesUnsaved)

            if sel2 == 'add' and continueProgram and continueHotspots:
                hotspotList, hotspotIDList, changesUnsaved = pgf.addLinkHotspotMenu(hotspotList, hotspotIDList, imageList, initYaw, changesUnsaved)
            elif sel2 == 'edit' and continueProgram and continueHotspots:
                hotspotList, hotspotIDList, changesUnsaved = pgf.editLinkHotspotMenu(hotspotList, hotspotIDList, modifiedHotspotID, imageList, changesUnsaved)
            elif sel2 == 'del' and continueProgram and continueHotspots:
                hotspotList, hotspotIDList, changesUnsaved = pgf.deleteHotspotPopup(hotspotList, hotspotIDList, modifiedHotspotID, imageSelected, 'Link', changesUnsaved)
            elif sel2 == 'save' and continueProgram and continueHotspots:
                uhf.implementLinkChanges(mainDirPath, imageSelected, hotspotList)
                changesUnsaved = False

        if changesUnsaved: # Checks if changes are saved, if not ask the user, this will occur on exit and on 'Going Back'
            saveSelection = pgf.saveChangesPopup()
            if saveSelection == 'y':
                uhf.implementLinkChanges(mainDirPath, imageSelected, hotspotList) # Save changes if chosen by user

    elif selection == 'info' and continueProgram:
        imageList = pgf.listTourImages(mainDirPath)
        imageSelected, continueProgram, goBack = pgf.selectFromListMenu('Edit Info Hotspots', 'Select Image Data to Edit:', imageList)

        changesUnsaved = False
        continueHotspots = True
        if continueProgram and not goBack:
            hotspotList, infoTitleList, initYaw = uhf.listInfoHotspots(mainDirPath, imageSelected)
        while continueProgram and continueHotspots and not goBack:
            sel2, modifiedHotspotID, continueProgram, continueHotspots = pgf.hotspotMenu(imageSelected, infoTitleList, changesUnsaved)

            if sel2 == 'add' and continueProgram and continueHotspots:
                hotspotList, infoTitleList, changesUnsaved = pgf.addInfoHotspotMenu(hotspotList, infoTitleList, initYaw, changesUnsaved)
            elif sel2 == 'edit' and continueProgram and continueHotspots:
                hotspotList, infoTitleList, changesUnsaved = pgf.editInfoHotspotMenu(hotspotList, infoTitleList, modifiedHotspotID, changesUnsaved)
            elif sel2 == 'del' and continueProgram and continueHotspots:
                hotspotList, infoTitleList, changesUnsaved = pgf.deleteHotspotPopup(hotspotList, infoTitleList, modifiedHotspotID, imageSelected, 'Info', changesUnsaved)
            elif sel2 == 'save' and continueProgram and continueHotspots:
                uhf.implementInfoChanges(mainDirPath, imageSelected, hotspotList)
                changesUnsaved = False

        if changesUnsaved: # Checks if changes are saved, if not ask the user, this will occur on exit and on 'Going Back'
            saveSelection = pgf.saveChangesPopup()
            if saveSelection == 'y':
                uhf.implementInfoChanges(mainDirPath, imageSelected, hotspotList) # Save changes if chosen by user