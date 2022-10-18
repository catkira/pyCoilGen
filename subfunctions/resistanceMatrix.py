import numpy as np
from .defineTargetField import distanceBetweenPoints

def getResistanceMatrix(mesh,materialFactor):
    '''returns the resistance Matrix for the given mesh'''
    nodeAdjacencyMatrix=getNeighbourhoodMatrix(mesh)
    #nodeAdjacencyMatrix = nodeAdjacencyMatrix | np.matrix.getH(nodeAdjacencyMatrix)
    neighbourPairs = np.array(np.where(nodeAdjacencyMatrix))
    neighbourPairs = neighbourPairs[:,neighbourPairs[1].argsort()]
   
    matElementsShouldGetValue = [np.concatenate([np.linspace(0,263,264),neighbourPairs[0]]) ,np.concatenate([np.linspace(0,263,264),neighbourPairs[1]])] 
    #matElementsShouldGetValue = neighbourPairs
    with open('test2.txt', 'w') as f:
        for i in range(len(matElementsShouldGetValue[0])):
            f.write("[0]" + str(matElementsShouldGetValue[0][i]) + "[1]" + str(matElementsShouldGetValue[1][i]))
            f.write('\n')
    # #useless at this position ...
    # nodeAdjacencyMatrix = nodeAdjacencyMatrix | np.matrix.getH(nodeAdjacencyMatrix)
    
    # #calc matrix of spatial distances - at the Moment not needed anywhere ...
    # nodalNeighbourMatrix = getSpatialDistancesMatrix(mesh)
    
    resistanceMatrix = np.zeros((len(mesh.vertices),len(mesh.vertices)),dtype=float)
    
    for elementIndex in range(len(matElementsShouldGetValue[0])):
        nodeInd1 = int(matElementsShouldGetValue[0][elementIndex])
        nodeInd2 = int(matElementsShouldGetValue[1][elementIndex])
        if nodeInd1 == nodeInd2:
            resistanceSum = 0
            for triangle in mesh.oneRingList[nodeInd1]:
                triangelArea = np.linalg.norm(np.cross((mesh.vertices[triangle[0]]-mesh.vertices[nodeInd1]),(mesh.vertices[triangle[1]]-mesh.vertices[nodeInd1])))/2
                current = (mesh.vertices[triangle[1]]-mesh.vertices[triangle[0]])/(np.linalg.norm(np.cross((mesh.vertices[triangle[0]]-mesh.vertices[nodeInd1]),(mesh.vertices[triangle[1]]-mesh.vertices[nodeInd1]))))
                resistanceSum = resistanceSum + np.dot(current,current)*triangelArea**2
            resistanceMatrix[nodeInd1][nodeInd1] = resistanceSum
        else:
            trianglesWithBothNodes = [elementInArray(mesh.oneRingList[nodeInd1],nodeInd2),elementInArray(mesh.oneRingList[nodeInd2],nodeInd1)]
            if trianglesWithBothNodes[0]:
                resistanceSum =0
                for triangle in trianglesWithBothNodes[0]:
                    triangelArea = np.linalg.norm(np.cross((mesh.vertices[triangle[0]]-mesh.vertices[nodeInd1]),(mesh.vertices[triangle[1]]-mesh.vertices[nodeInd1])))/2
                    primaryCurrent = (mesh.vertices[triangle[1]]-mesh.vertices[triangle[0]])/(np.linalg.norm(np.cross((mesh.vertices[triangle[0]]-mesh.vertices[nodeInd1]),(mesh.vertices[triangle[1]]-mesh.vertices[nodeInd1]))))
                    partnerElement = getPartnerElement(triangle,trianglesWithBothNodes,nodeInd2)
                    secondaryCurrent = (mesh.vertices[partnerElement[1]]-mesh.vertices[partnerElement[0]])/(np.linalg.norm(np.cross((mesh.vertices[partnerElement[0]]-mesh.vertices[nodeInd2]),(mesh.vertices[partnerElement[1]]-mesh.vertices[nodeInd2]))))
                    resistanceSum = resistanceSum + np.dot(primaryCurrent,secondaryCurrent)*(triangelArea**2)
                resistanceMatrix[nodeInd1][nodeInd2] = resistanceSum
    resistanceMatrix = resistanceMatrix + np.transpose(resistanceMatrix)
    resistanceMatrix = resistanceMatrix*materialFactor
    return resistanceMatrix

def getPartnerElement(triangle,trianglesWithBothNodes,nodeInd2):
    partnerElement =0
    for i in triangle: 
        if i != nodeInd2:
            differentElement = i
    for j in trianglesWithBothNodes[1]:
        if differentElement in j:
            partnerElement = j
    return partnerElement

def elementInArray(array,value):
    '''returns a list with the elements the contain "value"'''
    solution =[]
    for element in array:
        if value in element:
            solution.append(element)
    return solution

def elementInAandB(a, b):
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
