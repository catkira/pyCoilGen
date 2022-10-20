import numpy as np
from defineTargetField import distanceBetweenPoints

def getResistanceMatrix(mesh,materialFactor):
    '''returns the resistance Matrix for the given mesh'''
    matElementsShouldGetValue = getMatElementShouldGetValue(mesh)
    resistanceMatrix = createPreviousResistanceMat(mesh,matElementsShouldGetValue)
    resistanceMatrix = formFinalResistanceMat(resistanceMatrix,materialFactor)
    return resistanceMatrix

def formFinalResistanceMat(resistanceMatrix,materialFactor):
    '''returns resistanceMatrix in final form. added with its transposed and multiplied with materialFactor'''
    resistanceMatrix = (resistanceMatrix + np.transpose(resistanceMatrix))*materialFactor
    return resistanceMatrix

def createPreviousResistanceMat(mesh,matElementsShouldGetValue):
    '''returns resistanceMatrix mit entries in matElementsShouldGetValue'''
    resistanceMatrix = np.zeros((len(mesh.vertices),len(mesh.vertices)),dtype=float)    
    for elementIndex in range(len(matElementsShouldGetValue[0])):
        nodeInd1 = int(matElementsShouldGetValue[0][elementIndex])
        nodeInd2 = int(matElementsShouldGetValue[1][elementIndex])
        if nodeInd1 == nodeInd2:
            resistanceSum = getResistanceSumForSame(mesh,nodeInd1)
            resistanceMatrix[nodeInd1][nodeInd1] = resistanceSum
        else:
            trianglesWithBothNodes = [elementInArray(mesh.oneRingList[nodeInd1],nodeInd2),elementInArray(mesh.oneRingList[nodeInd2],nodeInd1)]
            resistanceSum = getResistanceSumForDifferent(mesh,trianglesWithBothNodes,nodeInd1,nodeInd2)
            resistanceMatrix[nodeInd1][nodeInd2] = resistanceSum
    return resistanceMatrix

def getResistanceSumForDifferent(mesh,trianglesWithBothNodes,nodeInd1,nodeInd2):   
    '''returns resistanceSum for the Case node1 and node2 are different''' 
    resistanceSum =0
    for triangle in trianglesWithBothNodes[0]:
        triangelArea = calculateArea(mesh.vertices[nodeInd1],mesh.vertices[triangle[0]],mesh.vertices[triangle[1]])
        primaryCurrent = calculateCurrent(mesh.vertices[nodeInd1],mesh.vertices[triangle[0]],mesh.vertices[triangle[1]])
        partnerElement = getPartnerElement(triangle,trianglesWithBothNodes,nodeInd2)
        secondaryCurrent = calculateCurrent(mesh.vertices[nodeInd2],mesh.vertices[partnerElement[0]],mesh.vertices[partnerElement[1]])
        resistanceSum = resistanceSum + np.dot(primaryCurrent,secondaryCurrent)*(triangelArea**2)
    return resistanceSum

def getResistanceSumForSame(mesh,nodeInd1):
    '''returns resistanceSum for the Case node1 and node2 are the same'''
    resistanceSum = 0
    for triangle in mesh.oneRingList[nodeInd1]:
        triangelArea = calculateArea(mesh.vertices[nodeInd1],mesh.vertices[triangle[0]],mesh.vertices[triangle[1]])
        current = calculateCurrent(mesh.vertices[nodeInd1],mesh.vertices[triangle[0]],mesh.vertices[triangle[1]])
        resistanceSum = resistanceSum + np.dot(current,current)*triangelArea**2
    return resistanceSum

def calculateArea(Point1,Point2,Point3):
    '''returns the area of a triangle with 3 given Points'''
    return np.linalg.norm(np.cross((Point2-Point1),(Point3-Point1)))/2

def calculateCurrent(Point1, Point2, Point3):
    '''returns the current of a triangle with 3 given Points'''
    return (Point3-Point2)/(np.linalg.norm(np.cross((Point2-Point1),(Point3-Point1))))

def getMatElementShouldGetValue(mesh):
    '''returns a list with positions in the matix that should get a value (diagonal elements == same nodes and neighbouring nodes)'''
    nodeAdjacencyMatrix = getNeighbourhoodMatrix(mesh)
    neighbourPairs = np.array(np.where(nodeAdjacencyMatrix))
    neighbourPairs = neighbourPairs[:,neighbourPairs[1].argsort()]   
    matElementsShouldGetValue = [np.concatenate([np.linspace(0,263,264),neighbourPairs[0]]) ,np.concatenate([np.linspace(0,263,264),neighbourPairs[1]])] 
    return matElementsShouldGetValue

def getPartnerElement(triangle,trianglesWithBothNodes,nodeInd2):
    '''returns the specified triangle both nodes are in from the oneRingList of the other one node. Important because different Point-orders cause different currents.'''
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

