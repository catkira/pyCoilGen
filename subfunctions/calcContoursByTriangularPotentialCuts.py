import numpy as np
from .readMesh import updateList

def calcContoursByTriangluarPotentialCuts(mesh,potentialLevelList,streamFunction):

    edges = getEdges(mesh)
    edgeAttachedTriangles = getEdgeAttachedTriangles(edges,mesh)
    numAttachedTriangles = getNumAttachedTriangles(edgeAttachedTriangles)
    innerEdges, innerEdgesTrianglesInds = getInnerEdges(edges,numAttachedTriangles,edgeAttachedTriangles)
    innerEdgeTriangleNodes = getInnerEdegTriangleNodes(innerEdgesTrianglesInds,mesh)
    innerEdgeOpposedNode = getEdgeOpposedNode(innerEdgeTriangleNodes,innerEdges)

    contourLevelList = potentialLevelList
    edgeNodePotentials = streamFunction[innerEdges]
    minEdgePotential=[]
    maxEgdePotential = []
    for x in range(len(edgeNodePotentials)):
        minEdgePotential.append(min(edgeNodePotentials[x]))
        maxEgdePotential.append(max(edgeNodePotentials[x]))
    triBelowPotStep = []
    triAbovePotStep = []
    for i in range(len(maxEgdePotential)):
        triBelowPotStep.append(maxEgdePotential[i]>contourLevelList)
        triAbovePotStep.append(minEdgePotential[i]<contourLevelList)
    potentialCutCriteria = np.array(triBelowPotStep) & np.array(triAbovePotStep)
    innerEdges = np.array(innerEdges)
    edgeLength = np.sqrt((mesh.u[innerEdges[:,0]]-mesh.u[innerEdges[:,1]])**2 + (mesh.v[innerEdges[:,0]]-mesh.v[innerEdges[:,1]])**2)
    edgePotentialSpan = edgeNodePotentials[:,1]-edgeNodePotentials[:,0]

    potDistToStep = []
    cutPointDistanceToEdgeNode=[]
    for x in range(len(edgeNodePotentials)):
        potDistToStepPart = []
        cutPointDistanceToEdgeNodePart = []
        for y in range(len(contourLevelList)):
            potDistToStepPart.append(contourLevelList[y]-edgeNodePotentials[x][0])
            cutPointDistanceToEdgeNodePart.append(np.abs(edgeLength[x]/edgePotentialSpan[x] * (contourLevelList[y]-edgeNodePotentials[x][0])))
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
                listelement.append([uCutPoint[edgeInd][potInd],vCutPoint[edgeInd][potInd],edgeInd])
        potentialSortedCutPoints.append(listelement)



    contours=0
    return contours

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
