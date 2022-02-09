# File: Hotspot.py
# By: Sebastian Alessandrino
# Date Created: 01/02/2022
# Purpose: Abstract Class defined to be used by either LinkHotspots or InfoHotspots

from abc import ABC, abstractmethod # abc = abstract base class
import math

# Relative yaw is based on where the initial view of the image in a map is set compared to the location of the hotspot
# This will be used to simplify the process of choosing a location for new hotspots
# Relative pitch is not required as this can be determined quite easily without a relative value
class Hotspot(ABC):
    initYaw = 0
    relativeYaw = 0
    trueYaw = 0
    truePitch = 0

    def __init__(self, initYaw, trueYaw, truePitch):
        self.initYaw = initYaw
        self.relativeYaw = self.calcRelativeYaw(initYaw, trueYaw)
        self.trueYaw = trueYaw
        self.truePitch = truePitch
        # These values are stored in radians

    # SETTERS
    # Recieves a yaw in degrees and sets it in radians
    def setTrueYaw(self, relYawInDeg):
        valueSet = False
        if self.validateYawDegrees(relYawInDeg):
            relYaw = relYawInDeg * math.pi / 180.0
            self.relativeYaw = relYaw
            self.trueYaw = self.calcTrueYaw(relYaw)
            valueSet = True
        return valueSet
    
    # Receives a pitch in degrees and sets it in radians
    def setTruePitch(self, pitchInDeg):
        valueSet = False
        if self.validatePitchDegrees(pitchInDeg):
            pitch = pitchInDeg * math.pi / 180.0
            self.truePitch = pitch
            valueSet = True
        return valueSet

    # GETTERS
    def getInitYaw(self):
        return self.initYaw

    def getRelativeYaw(self):
        return self.relativeYaw

    def getTrueYaw(self):
        return self.trueYaw

    def getTruePitch(self):
        return self.truePitch

    # Returns the relative yaw in degrees
    def getRelativeYawDegrees(self):
        return self.relativeYaw * 180.0 / math.pi

    # Returns the true yaw in degrees
    def getTrueYawDegrees(self):
        return self.trueYaw * 180.0 / math.pi
    
    # Returns the true pitch in degrees
    def getTruePitchDegrees(self):
        return self.truePitch * 180.0 / math.pi

    @abstractmethod
    def toString(self):
        pass

    # Determines yaw of hotspot when calculated from an initial position (an initial view position in map project)
    def calcRelativeYaw(self, ref, true):
        relativeYaw = true - ref
        if relativeYaw > math.pi:
            relativeYaw -= math.pi * 2
        elif relativeYaw < - math.pi:
            relativeYaw += math.pi * 2
        return relativeYaw

# Calculates the true yaw based on the given relative yaw and the class' init yaw (which corresponds to the image)
    def calcTrueYaw(self, rel):
        trueVal = self.initYaw + rel
        if trueVal > math.pi:
            trueVal -= math.pi * 2
        elif trueVal < - math.pi:
            trueVal += math.pi * 2
        return trueVal

    # Ensures the value given in degrees is between -180 and 180 degrees
    def validateYawDegrees(self, yaw):
        valid = False
        if yaw <= 180.0 and yaw > -180.0:
            valid = True
        return valid

    # Ensures the value given in degrees is between -90 and 90 degrees
    def validatePitchDegrees(self, pitch):
        valid = False
        if pitch <= 90.0 and pitch > -90.0:
            valid = True
        return valid