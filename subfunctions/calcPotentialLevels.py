import numpy as np

def calcPotentialLevels(streamFunction, numLevels, levelOffset):
    '''returns the contourStep and the potentialLevelList. more options need to be implemented, if there is more than one mesh.'''
    SFRangePerMesh = np.max(streamFunction)-np.min(streamFunction)
    contourStep = SFRangePerMesh/(numLevels-1+2*levelOffset)
    potentialLevelList= np.arange(0,numLevels)*contourStep+(np.min(streamFunction)+levelOffset*contourStep)

    # if levelSetMethode == "primary":
    #     primaryMethode(streamFunction,numLevels,levelOffset)

    # elif levelSetMethode == "combined":
    #     contourStep, potentialLevelList = combinedMethode(streamFunction,numLevels,levelOffset)
    #     primarySurfaceInd  = 1

    return contourStep, potentialLevelList #, primarySurfaceInd

# def primaryMethode(streamFunction,numLevels,levelOffset):
#     '''Applys the primary Methode (select the stream function of the part with the highest current density for the finding level width)'''
#     SFRangePerMesh = np.max(streamFunction)-np.min(streamFunction)
#     contourStep = SFRangePerMesh/(numLevels-1+2*levelOffset)
#     potentialLevelList= np.arange(0,numLevels)*contourStep+(min(streamFunction)+levelOffset*contourStep)


#  def combinedMethode(streamFunction,numLevels,levelOffset):
#     '''Depending on what stream function is inserted, levels for the combined mesh or each individual part are found'''
#     contourStep = (max(streamFunction) - min(streamFunction)) / (numLevels-1 +2*levelOffset)
#     potentialLevelList = (np.linspace(1,numLevels,numLevels) - (1-levelOffset))*contourStep + min(streamFunction)
#     return contourStep, potentialLevelList



