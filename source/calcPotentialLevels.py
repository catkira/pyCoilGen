import numpy as np

def calcPotentialLevels(streamFunction, numLevels, levelOffset):
    '''returns the contourStep and the potentialLevelList. more options need to be implemented, if there is more than one mesh.'''
    SFRangePerMesh = np.max(streamFunction)-np.min(streamFunction)
    contourStep = SFRangePerMesh/(numLevels-1+2*levelOffset)
    potentialLevelList= np.arange(0,numLevels)*contourStep+(np.min(streamFunction)+levelOffset*contourStep)

    return contourStep, potentialLevelList 