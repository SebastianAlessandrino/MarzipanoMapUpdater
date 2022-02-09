# File: LinkHotspot.py
# By: Sebastian Alessandrino
# Date Created: 01/02/2022
# Purpose: Class inheriting from Hotspot class to be used for storing data about link hotspots when editting them in the map update project

from Hotspot import Hotspot

class LinkHotspot(Hotspot):
    target = ''

    def __init__(self, initYaw, trueYaw, truePitch, target):
        super().__init__(initYaw, trueYaw, truePitch)
        self.target = target

    # Getter
    def setTarget(self, newTarget):
        self.target = newTarget

    # Setter
    def getTarget(self):
        return self.target

    # Produces the string that would be a hotspot entry in a data.js file
    def toString(self):
        outStr = "        {\n" + f"          \"yaw\": {super().getTrueYaw()},\n" + f"          \"pitch\": {super().getTruePitch()},\n" + "          \"rotation\": 0,\n"
        outStr += f"          \"target\": \"{self.target}\"\n" + "        }"
        return outStr