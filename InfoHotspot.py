# File: InfoHotspot.py
# By: Sebastian Alessandrino
# Date Created: 01/02/2022
# Purpose: Class inheriting from Hotspot class to be used for storing data about info hotspots when editting them in the map update project

from Hotspot import Hotspot

class InfoHotspot(Hotspot):
    title = ''
    text = ''
    
    def __init__(self, initYaw, trueYaw, truePitch, title, text):
        super().__init__(initYaw, trueYaw, truePitch)
        self.title = title
        self.text = text

    # Getters
    def setTitle(self, newTitle):
        self.title = newTitle

    def setText(self, newText):
        self.text = newText

    # Setters
    def getTitle(self):
        return self.title

    def getText(self):
        return self.text

    # Produces the string that would be a hotspot entry in a data.js file
    def toString(self):
        outStr = "        {\n" + f"          \"yaw\": {super().getTrueYaw()},\n" + f"          \"pitch\": {super().getTruePitch()},\n" + f"          \"title\": \"{self.title}\",\n"
        outStr += f"          \"text\": \"{self.text}\"\n" + "        }"
        return outStr