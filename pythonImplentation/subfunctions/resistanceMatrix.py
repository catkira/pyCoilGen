import numpy as np
from .defineTargetField import distanceBetweenPoints

def getResistanceMatrix(mesh,materialFactor):
    '''returns the resistance Matrix for the given mesh'''
    
    # get neighbours nodes 
    neighbourPairs = np.where(getNeighbourhoodMatrix(mesh)) # vert2 == vert[0] (matlab Implementation)

    # define matrix elements that should get a value (neighbours + diagonal elements)
    meshEdgesNonUnique = [np.concatenate([np.linspace(0,263,264),neighbourPairs[1]]) ,np.concatenate([np.linspace(0,263,264),neighbourPairs[0]]) ]

    # #useless at this position ...
    # nodeAdjacencyMatrix = nodeAdjacencyMatrix | np.matrix.getH(nodeAdjacencyMatrix)
    
    # #calc matrix of spatial distances - at the Moment not needed anywhere ...
    # nodalNeighbourMatrix = getSpatialDistancesMatrix(mesh)
    
    #calc resistance matrix
    resistanceMatrix = np.zeros((len(mesh.vertices),len(mesh.vertices)),dtype=float)
    #look at each "want to change" matrix positions
    for edgeInd in range(len(meshEdgesNonUnique[0])):
        nodeInd1 = int(meshEdgesNonUnique[0][edgeInd])
        nodeInd2 = int(meshEdgesNonUnique[1][edgeInd])
        #find the triangles that surround both nodes
        overlappingTriangles = intersect_mtlb(mesh.neighbours[nodeInd1],mesh.neighbours[nodeInd2])
        resistanceSum =0
        if overlappingTriangles:
            for overlappTriangle in overlappingTriangles:
                firstNodeTrianglePosition = compareMultipleElementsBoolean(mesh.neighbours[nodeInd1],overlappTriangle)
                secondNodeTrianglePosition = compareMultipleElementsBoolean(mesh.neighbours[nodeInd2],overlappTriangle)
                triangelArea = mesh.areas[overlappTriangle]

                primaryCurrent,secondaryCurrent = [0,0,0],[0,0,0]
                for i in range(len(mesh.neighbourcurrents[nodeInd1])):
                    primaryCurrent += mesh.neighbourcurrents[nodeInd1][i]*firstNodeTrianglePosition[i]
                for i in range(len(mesh.neighbourcurrents[nodeInd2])):
                    secondaryCurrent += mesh.neighbourcurrents[nodeInd2][i]*secondNodeTrianglePosition[i]
                resistanceSum += np.dot(primaryCurrent,secondaryCurrent)*triangelArea**2
            resistanceMatrix[nodeInd1][nodeInd2] = resistanceSum
    resistanceMatrix = 2*resistanceMatrix*materialFactor
    return resistanceMatrix


def intersect_mtlb(a, b):
    '''returns a list with elements that are in a and b'''
    solution =[]
    for i in a:
        if i in b: solution.append(i)
    return solution


def compareMultipleElementsBoolean(elements,testelements):
    '''returns a array with boolean elements in the length of elements, True if the value is in testelements False otherwise'''
    comparisonResult=[]
    for i in elements:
        if i == testelements:
            comparisonResult.append(True)
        else: 
            comparisonResult.append(False)
    return comparisonResult


def getSpatialDistancesMatrix(mesh):
    '''returns a matrix containing the spatial distance between node i and node j'''
    nodalNeighbourMatrix = np.full((len(mesh.vertices),len(mesh.vertices)), 0,dtype=float)
    for i in range(len(mesh.vertices)):
        for j in range(len(mesh.vertices)):
            nodalNeighbourMatrix[i][j] = distanceBetweenPoints(mesh.vertices[i],mesh.vertices[j])
    return nodalNeighbourMatrix


def getNeighbourhoodMatrix(mesh):
    '''returns a boolean matrix with information if node i and node j are neighbours'''
    nodeAdjacencyMatrix = np.full((len(mesh.vertices),len(mesh.vertices) ), False)
    for i in range(len(mesh.faces)):
        nodeAdjacencyMatrix[mesh.faces[i][0]][mesh.faces[i][1]]=True
        nodeAdjacencyMatrix[mesh.faces[i][1]][mesh.faces[i][2]]=True
        nodeAdjacencyMatrix[mesh.faces[i][2]][mesh.faces[i][0]]=True
    return nodeAdjacencyMatrix



def compareMultipleElementsBooleanTest():
    '''Test function: should always be True'''
    return len(np.where(compareMultipleElementsBoolean()))==1

def triangleAreaTest(): # muss noch eingebaut werden (?) TODO: Nachlesen PyTest
    '''Test function: should alway be True'''
    return (mesh.areas[overlappTriangle] ==  max(mesh.neighbourareas[nodeInd1]* np.array(firstNodeTrianglePosition)))
