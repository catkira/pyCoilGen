import numpy as np

def calcPotentialLevels(streamFunction, numLevels, levelOffset, levelSetMethode):

    if levelSetMethode == "primary":
        primaryMethode()

    elif levelSetMethode == "combined":
        contourStep, potentialLevelList = combinedMethode(streamFunction,numLevels,levelOffset)
        primarySurfaceInd  = 1

    return contourStep, potentialLevelList, primarySurfaceInd

def primaryMethode():#WIP
    '''Applys the primary Methode (select the stream function of the part with the highest current density for the finding level width)'''

def combinedMethode(streamFunction,numLevels,levelOffset):
    '''Depending on what stream function is inserted, levels for the combined mesh or each individual part are found'''
    contourStep = (max(streamFunction) - min(streamFunction)) / (numLevels-1 +2*levelOffset)
    potentialLevelList = (np.linspace(1,numLevels,numLevels) - (1-levelOffset))*contourStep + min(streamFunction)
    return contourStep, potentialLevelList



