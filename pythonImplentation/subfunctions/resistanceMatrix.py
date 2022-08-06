import numpy as np
from .defineTargetField import distanceBetweenPoints

specificConductivityMaterial = 1.8000*10**-8
conducterThickness = 0.005 #Werte von Philipp abgeschrieben 
materialFactor = specificConductivityMaterial/conducterThickness

def getResistanceMatrix(mesh):
    #create a matrix for neighbourhood or not
    nodeAdjacencyMatrix = np.full((len(mesh.vertices),len(mesh.vertices) ), False)
    for i in range(len(mesh.faces)):
        nodeAdjacencyMatrix[mesh.faces[i][0]][mesh.faces[i][1]]=True
        nodeAdjacencyMatrix[mesh.faces[i][1]][mesh.faces[i][2]]=True
        nodeAdjacencyMatrix[mesh.faces[i][2]][mesh.faces[i][0]]=True
    nodeAdjacencyMatrix = nodeAdjacencyMatrix | np.matrix.getH(nodeAdjacencyMatrix)

    vert = np.argwhere(nodeAdjacencyMatrix)
    meshEdgesNonUnique=[]
    for j in range(len(vert)):
        meshEdgesNonUnique.append([vert[j][0],vert[j][1]]) #ich weiß nicht, was die zählwerte in Matlab machen 
    
    #calc matrix of spatial distances
    nodalNeighbourMatrix = np.full((len(mesh.vertices),len(mesh.vertices)), 0)
    for i in range(len(mesh.vertices)):
        for j in range(len(mesh.vertices)):
            if nodeAdjacencyMatrix[i][j]:
                nodalNeighbourMatrix[i][j] = distanceBetweenPoints(mesh.vertices[i],mesh.vertices[j])
    
    #calc resistance matrix
    resistanceMatrix = np.zeros((len(mesh.vertices),len(mesh.vertices)))
    for edgeInd in range(len(meshEdgesNonUnique)):
        #gleiche Dreiecke benachbarter Knotenpunkte 
        nodeInd1 = meshEdgesNonUnique[edgeInd][0]
        nodeInd2 = meshEdgesNonUnique[edgeInd][1]
        overlappingTriangles = np.intersect1d(mesh.neighbours[nodeInd1],mesh.neighbours[nodeInd2])#evtl Faktor(?) abgeschnitten
        resistanceSum =0
        for overlappTriangle in overlappingTriangles:
            firstNodeTrianglePosition = mesh.neighbours[nodeInd1] == overlappTriangle
            secondNodeTrianglePosition = mesh.neighbours[nodeInd2]== overlappTriangle
            triangelArea = max(mesh.areas[nodeInd1]* firstNodeTrianglePosition)
            
            for i in range(len(mesh.neighbourcurrents[nodeInd1])):
                if np.array_equal(mesh.neighbourcurrents[nodeInd1][i]*firstNodeTrianglePosition[i] , [0,0,0]) == False:
                    primaryCurrent = mesh.neighbourcurrents[nodeInd1][i]*firstNodeTrianglePosition[i]
            for i in range(len(mesh.neighbourcurrents[nodeInd2])):
                if np.array_equal(mesh.neighbourcurrents[nodeInd2][i]*secondNodeTrianglePosition[i] , [0,0,0]) == False:
                    secondaryCurrent = mesh.neighbourcurrents[nodeInd2][i]*secondNodeTrianglePosition[i]
            resistanceSum += np.dot(primaryCurrent,secondaryCurrent)*triangelArea**2
        resistanceMatrix[nodeInd1][nodeInd2] = resistanceSum
    resistanceMatrix = 2*resistanceMatrix*materialFactor
    return resistanceMatrix