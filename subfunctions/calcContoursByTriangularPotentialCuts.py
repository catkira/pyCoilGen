import numpy as np
from .readMesh import updateList

def calcContoursByTriangluarPotentialCuts(mesh,potentialLevelList,streamFunction):

    edges = getEdges(mesh)
    edgeAttachedTriangles = getEdgeAttachedTriangles(edges,mesh)
    numAttachedTriangles = getNumAttachedTriangles(edgeAttachedTriangles)
    innerEdges, innerEdgesTrianglesInds = getInnerEdges(edges,numAttachedTriangles,edgeAttachedTriangles)
    innerEdgeTriangleNodes = getInnerEdegTriangleNodes(innerEdgesTrianglesInds,mesh)
    innerEdgeOpposedNode = getEdgeOpposedNode(innerEdgeTriangleNodes,innerEdges)

    edgeNodePotentials = streamFunction[innerEdges]
    potentialCutCriteria = getPotentialCutCriteria(edgeNodePotentials,potentialLevelList)
    innerEdges = np.array(innerEdges)
    edgeLength = np.sqrt((mesh.u[innerEdges[:,0]]-mesh.u[innerEdges[:,1]])**2 + (mesh.v[innerEdges[:,0]]-mesh.v[innerEdges[:,1]])**2)
    edgePotentialSpan = edgeNodePotentials[:,1]-edgeNodePotentials[:,0]

    potDistToStep = []
    cutPointDistanceToEdgeNode=[]
    for x in range(len(edgeNodePotentials)):
        potDistToStepPart = []
        cutPointDistanceToEdgeNodePart = []
        for y in range(len(potentialLevelList)):
            potDistToStepPart.append(potentialLevelList[y]-edgeNodePotentials[x][0])
            cutPointDistanceToEdgeNodePart.append(np.abs(edgeLength[x]/edgePotentialSpan[x] * (potentialLevelList[y]-edgeNodePotentials[x][0])))
        potDistToStep.append(potDistToStepPart)
        cutPointDistanceToEdgeNode.append(cutPointDistanceToEdgeNodePart)

    uKompEdgeVec = mesh.u[innerEdges[:,1]] - mesh.u[innerEdges[:,0]]
    vKompEdgeVec = mesh.v[innerEdges[:,1]] - mesh.v[innerEdges[:,0]]
    uCutPoint,vCutPoint=[],[]
    for x in range(len(edgeLength)):
        uCutPoint.append(potentialCutCriteria[x] * (mesh.u[innerEdges[:,0]][x] + cutPointDistanceToEdgeNode[x]/edgeLength[x] *uKompEdgeVec[x]))
        vCutPoint.append(potentialCutCriteria[x] * (mesh.v[innerEdges[:,0]][x] + cutPointDistanceToEdgeNode[x]/edgeLength[x] *vKompEdgeVec[x]))
    
    potentialSortedCutPoints = []
    for potInd in range(len(potentialLevelList)):
        listelement = []
        for edgeInd in range(len(uCutPoint)):
            if uCutPoint[edgeInd][potInd] != 0:
                listelement.append([uCutPoint[edgeInd][potInd],vCutPoint[edgeInd][potInd],int(edgeInd)])
        potentialSortedCutPoints.append(listelement)

    rawUnsortedPoints = []
    for i in range(len(potentialLevelList)):
        rawUnsortedPointsDict = {
            "potential": potentialLevelList[i],
            "edgeInd": np.array(potentialSortedCutPoints[i])[:,2].astype(int),
            "uv": [np.array(potentialSortedCutPoints[i])[:,0],np.array(potentialSortedCutPoints[i])[:,1]],
        }
        rawUnsortedPoints.append(rawUnsortedPointsDict)

    rawUnarrangedLoops = getRawUnarrangedLoops(rawUnsortedPoints,innerEdges,innerEdgeOpposedNode)
 
    #TODO: next step Matlab calc_contours_by trianglar_potential_cuts line 179 "evaluate for each loop the current orientation"

    contours=0
    return contours

def getPotentialCutCriteria(edgeNodePotentials,potentialLevelList):
    minEdgePotential=[]
    maxEgdePotential = []
    for x in range(len(edgeNodePotentials)):
        minEdgePotential.append(min(edgeNodePotentials[x]))
        maxEgdePotential.append(max(edgeNodePotentials[x]))
    triBelowPotStep = []
    triAbovePotStep = []
    for i in range(len(maxEgdePotential)):
        triBelowPotStep.append(maxEgdePotential[i]>potentialLevelList)
        triAbovePotStep.append(minEdgePotential[i]<potentialLevelList)
    return np.array(triBelowPotStep) & np.array(triAbovePotStep)

def getRawUnarrangedLoops(rawUnsortedPoints,innerEdges,innerEdgeOpposedNode):
    '''returns rawUnarrangedLoops'''
    rawUnarrangedLoopsTotal = []
    for potentialGroupInd in range(len(rawUnsortedPoints)):
            allCurrentEdges = innerEdges[rawUnsortedPoints[potentialGroupInd]['edgeInd']]
            allCurrentOpposedNodes = np.array(innerEdgeOpposedNode)[rawUnsortedPoints[potentialGroupInd]['edgeInd']]
            allCurrentUVKoords = rawUnsortedPoints[potentialGroupInd]['uv']
            setNewStart = True
            numBuildLoops = 0
            edgeAlreadyUsed = np.zeros(len(allCurrentEdges))
            rawUnarrangedLoops = []

            while not edgeAlreadyUsed.all():
                if setNewStart:
                    oneLoop =[]
                    numBuildLoops += 1
                    startingEdge = min(np.argwhere(edgeAlreadyUsed== 0))
                    rawUnarrangedLoopsDict = {
                        "edgeInd":allCurrentEdges[startingEdge],
                        "uv": np.array(allCurrentUVKoords)[:,startingEdge]
                    }
                    oneLoop.append(rawUnarrangedLoopsDict)
                    edgeAlreadyUsed[startingEdge] = 1
                    currentEdge = startingEdge

                    testElement,testtestElement=checkIfPositionsElementIdenticalWithFirstList(allCurrentEdges,allCurrentOpposedNodes, currentEdge)
                    neighbouringFreeNextEdges = np.argwhere(np.any(testElement, axis=1) & np.any(testtestElement, axis=1))
                    if not neighbouringFreeNextEdges.any(): break
                    elif len(neighbouringFreeNextEdges) == 1: 
                        setNewStart = False
                        nextEdge = neighbouringFreeNextEdges[0]
                    else: 
                        setNewStart = False
                        if not edgeAlreadyUsed[neighbouringFreeNextEdges[0]]: nextEdge = neighbouringFreeNextEdges[0]
                        else: nextEdge = neighbouringFreeNextEdges[1]
                
                while not (nextEdge == startingEdge):
                    rawUnarrangedLoopsDict = {
                        "edgeInd":allCurrentEdges[nextEdge],
                        "uv": np.array(allCurrentUVKoords)[:,nextEdge]
                    }
                    oneLoop.append(rawUnarrangedLoopsDict)
                    edgeAlreadyUsed[nextEdge] = 1
                    currentEdge = np.copy(nextEdge)
            
                    testElement,testtestElement=checkIfPositionsElementIdenticalWithFirstList(allCurrentEdges,allCurrentOpposedNodes, currentEdge)
                    possibleNextEdges = np.argwhere(np.any(testElement, axis=1) & np.any(testtestElement, axis=1))
                    possibleNextEdges = np.setdiff1d(possibleNextEdges,np.argwhere(edgeAlreadyUsed == 1))
                    if not possibleNextEdges.any(): 
                        rawUnarrangedLoops.append(oneLoop)
                        break
                    elif len(possibleNextEdges) == 1: nextEdge = possibleNextEdges[0]
                    else: 
                        if not edgeAlreadyUsed[possibleNextEdges[0]]: nextEdge = possibleNextEdges[0]
                        else: nextEdge = possibleNextEdges[1]
                setNewStart = True 
            rawUnarrangedLoopsTotal.append(rawUnarrangedLoops)
    return rawUnarrangedLoopsTotal

def checkIfPositionsElementIdenticalWithFirstList(allCurrentEdges, allCurrentOpposedNodes, checkPosition):
    '''returns lists of elements with booleans if checkPostions Element of first and secound Element are identical with allCurrentEdges'''
    testElement=[]
    testtestElement=[]
    for i in allCurrentEdges:
        testElement1 =[]
        testElement2 =[]
        for j in i:
            testElement1.append(np.any(j == allCurrentOpposedNodes[checkPosition]))
            testElement2.append(np.any(j == allCurrentEdges[checkPosition]))
        testElement.append(testElement1)
        testtestElement.append(testElement2)
    return testElement,testtestElement

def getEdgeOpposedNode(innerEdgeTriangleNodes,innerEdges):
    '''returns the to the edge opposed node for each attached triangle'''
    edgeOpposedNodes = []
    for edgeInd in range(len(innerEdges)):
        oneEdgeOpposedNodes= []
        for triangleInd in range(len(innerEdgeTriangleNodes[edgeInd])):
            oneEdgeOpposedNodes.append(removeTwoElementsFromArray(innerEdgeTriangleNodes[edgeInd][triangleInd],innerEdges[edgeInd][0],innerEdges[edgeInd][1])[0])
        edgeOpposedNodes.append(oneEdgeOpposedNodes)
    return edgeOpposedNodes

def removeTwoElementsFromArray(array,Element1,Element2):
    '''returns the array without the two elements.'''
    return updateList(updateList(array,Element1),Element2)

def getInnerEdegTriangleNodes(innerEdgesTrianglesInds,mesh):
    '''returns the Node Indices for the Triangles.'''
    innerEdgeTriangleNodes = []
    for edgeInd in range(len(innerEdgesTrianglesInds)):
        innerEdgeTriangleNodes.append([np.array(mesh.faces[innerEdgesTrianglesInds[edgeInd][0]]),np.array(mesh.faces[innerEdgesTrianglesInds[edgeInd][1]])])
    return innerEdgeTriangleNodes

def getInnerEdges(edges,numAttachedTriangles,edgeAttachedTriangles):
    '''returns the inner edges an the corresponding triangleInds.'''
    innerEdges =[]
    innerEdgesTrianglesInds = []
    for index in range(len(edges)):
        if numAttachedTriangles[index] == 2:
            innerEdges.append(edges[index])
            innerEdgesTrianglesInds.append(edgeAttachedTriangles[index])
    return innerEdges, innerEdgesTrianglesInds

def getNumAttachedTriangles(edgeAttachedTriangles):
    '''returns the number of attached triangles per edge.'''
    numAttachedTriangles =[]
    for edgeInd in range(len(edgeAttachedTriangles)):
        numAttachedTriangles.append(len(edgeAttachedTriangles[edgeInd]))
    return numAttachedTriangles

def getEdgeAttachedTriangles(edges,mesh):
    '''returns the attached triangles for each edge.'''
    allEdgesTriangles=[]
    for edge in edges:
        edgeFaces =[]
        for triangleIndex in range(len(mesh.faces)):
            if edge[0] in mesh.faces[triangleIndex] and edge[1] in mesh.faces[triangleIndex]:
                edgeFaces.append(triangleIndex)
        allEdgesTriangles.append(edgeFaces)
    return allEdgesTriangles

def getEdges(mesh):
    '''returns all edges in the mesh.'''
    edges=[]
    for node in range(len(mesh.vertices)):
        for triangle in mesh.faces:
            if node in triangle:
                if node == triangle[0]:
                    if node < triangle[1] and [triangle[0],triangle[1]] not in edges:
                        edges.append([triangle[0],triangle[1]])
                    if node < triangle[2] and [triangle[0],triangle[2]] not in edges:
                        edges.append([triangle[0],triangle[2]])
                elif node == triangle[1]:
                    if node < triangle[0] and [triangle[1],triangle[0]] not in edges:
                        edges.append([triangle[1],triangle[0]])
                    if node < triangle[2] and [triangle[1],triangle[2]] not in edges:
                        edges.append([triangle[1],triangle[2]])
                elif node == triangle[2]:
                    if node < triangle[0] and [triangle[2],triangle[0]] not in edges:
                        edges.append([triangle[2],triangle[0]])
                    if node < triangle[1] and [triangle[2],triangle[1]] not in edges:
                        edges.append([triangle[2],triangle[1]])

    return edges
