import numpy as np
import scipy.linalg as sc

def streamFunctionOptimization(mesh,target,sensitivityMatrix,resistanceMatrix,tikonovFactor):
    '''returns the magnetic field generated by the optimized stream function. Version for only one coil part, else  a combined mesh is needed'''
    PotentialZeroAtBoundaryNodes = False

    sensitivityMatrixSingleZKomp=sensitivityMatrix[2]
    targetFieldSingleZKomp = target.fieldValues[2]

    redResMat,boundaryNodes,isNotBoundaryNode = reduceMatricesForBoundaryNodes(mesh,resistanceMatrix,PotentialZeroAtBoundaryNodes)
    redSenMat,boundaryNodes,isNotBoundaryNode = reduceMatricesForBoundaryNodes(mesh,sensitivityMatrixSingleZKomp,PotentialZeroAtBoundaryNodes)

    #scale tikonov regularization 
    tikonovFactor = tikonovFactor*np.shape(redSenMat)[0]/np.shape(redSenMat)[1]

    tikRegMat = tikonovFactor * redResMat
    reducedSF = np.dot(sc.pinv(np.dot(np.transpose(np.array(redSenMat)),redSenMat) + np.dot(np.transpose(np.array(tikRegMat)),tikRegMat)),np.dot(np.transpose(np.array(redSenMat)),np.transpose(targetFieldSingleZKomp)))

    #reexpand st stream fuction
    if PotentialZeroAtBoundaryNodes == False:
        optStreamFkt = reexpandSteamFunctionForBoundaryNodes(mesh,reducedSF,boundaryNodes,isNotBoundaryNode,PotentialZeroAtBoundaryNodes)
    else: optStreamFkt = reducedSF

    #calculate the magnetic field generated by the optimized stream function
    bFieldOptSF = [sensitivityMatrix[0]*optStreamFkt, sensitivityMatrix[1]*optStreamFkt, sensitivityMatrix[2]*optStreamFkt]

    #calc resulting current density of mesh faces
    updateMeshCurrentDensityFaces(mesh,optStreamFkt)
    return bFieldOptSF

def getReducedMat(mesh,dimToRed,reducedMat,zeroFlag):
    '''returns the reduced matrix'''
    boundaryNodes = [mesh.openBoundaries[1],mesh.openBoundaries[0]]
    for dimToRedInd in np.nonzero(dimToRed)[0]:
            index1=np.array([':']*np.ndim(reducedMat),dtype=object)
            index2=np.copy(index1)
            for boundaryInd in range(len(mesh.openBoundaries)):
                if zeroFlag:
                    index1[dimToRedInd] = boundaryNodes[boundaryInd][0]
                    reducedMat[index1[0:None]]=0
                else:
                    index1[dimToRedInd] = boundaryNodes[boundaryInd][0]
                    index2[dimToRedInd] = np.array(boundaryNodes[boundaryInd][0:None],dtype=int)
                    if dimToRedInd:#(==1)
                        reducedMat[:,(index1[1])] = np.sum(np.array(reducedMat)[:,index2[1]],dimToRedInd)#spalte ersetzen 
                    else:
                        reducedMat[index1[0]] = np.sum(np.array(reducedMat)[index2[0]],dimToRedInd)
    return reducedMat


def reduceMatricesForBoundaryNodes(mesh, matToRed,zeroFlag):
    dimToRed = getDimToRed(matToRed)
    boundaryNodes = [mesh.openBoundaries[1],mesh.openBoundaries[0]]
    numNodesPerBoundary = getNumNodesPerBoundary(mesh)  
    notBoundaryNodes = getNotBoundaryNodes(mesh)

    #reduction 
    if True not in dimToRed:
        print("nothing to reduce")
    else: 
        reducedMat = getReducedMat(mesh,dimToRed,matToRed,zeroFlag)

        #rearange the matrix to its reduces form
        boundaryNodesFirstInds = [boundaryNodes[i][0] for i in range(len(mesh.openBoundaries))]
        for dimToRedInd in np.nonzero(dimToRed)[0]:
            prevReducedMat = np.copy(reducedMat)
            index1=np.array([':']*np.ndim(matToRed),dtype=object)
            index2,index3,index4,index5 = np.copy(index1),np.copy(index1),np.copy(index1),np.copy(index1)
            index1[dimToRedInd] = [i for i in range(len(mesh.openBoundaries))]#passt
            index2[dimToRedInd] = [x-1 for x in boundaryNodesFirstInds]#passt
            index3[dimToRedInd] = np.arange((len(mesh.openBoundaries)),(len(notBoundaryNodes)+len(mesh.openBoundaries)))#passt
            new=[]
            for i in notBoundaryNodes:
                if i == 0:
                    new.append(len(matToRed))
                else: new.append(i)
            index4[dimToRedInd] = [x-1 for x in np.sort(new)]#passt
            index5[dimToRedInd] = np.arange(((len(matToRed[0])-(sum(numNodesPerBoundary)-len(mesh.openBoundaries)))), len(matToRed[0]))#passt

            
            if index1[0] == ':' and index2[0]==':' and index3[0] == ':' and index4[0]==':' and index5[0] == ':':
                reducedMat[:,index1[1]] = prevReducedMat[:,index2[1]]
                reducedMat[:,index3[1]] = prevReducedMat[:,index4[1]]
                reducedMat=np.delete(reducedMat,index5[1],1)
            else:
                reducedMat[index1[0]] = prevReducedMat[index2[0]]
                reducedMat[index3[0]] = prevReducedMat[index4[0]]
                reducedMat=np.delete(reducedMat,index5[0],0)
                
    return [reducedMat,boundaryNodes,notBoundaryNodes]

def getNotBoundaryNodes(mesh):
    '''returns no-boundary nodes of a given mesh'''
    isNotBoundaryNode = []
    for i in range(len(mesh.vertices[:,0])):
        if mesh.boundary[i]:
            continue
        else: isNotBoundaryNode.append(i)
    return isNotBoundaryNode

def getDimToRed(matToRed):
    '''returns boolean values which dimension should be reduced'''
    dimToRed=[]
    for i in np.shape(matToRed): 
        if i == len(matToRed[0]): dimToRed.append(True)
        else: dimToRed.append(False)
    return dimToRed

def getNumNodesPerBoundary(mesh):
    '''returns the number of nodes for every boundary'''
    numNodesPerBoundary=[]
    for i in range(len(mesh.openBoundaries)):
        numNodesPerBoundary.append(len(mesh.openBoundaries[i]))
    return numNodesPerBoundary

def reexpandSteamFunctionForBoundaryNodes(mesh,reducedSF,boundaryNodes,isNotBoundaryNode,zeroFlag):
    '''reexpand Streamfunction to all nodes, the nodes of the first boundary have a potential of zero'''
    streamFunction = np.zeros(len(mesh.vertices))
    for boundaryInd in range(len(boundaryNodes)):
        if zeroFlag:
            streamFunction[boundaryNodes[boundaryInd]]=0
        else:
            a = [x-1 for x in boundaryNodes[boundaryInd]]
            streamFunction[a]=reducedSF[boundaryNodes[boundaryInd]]
    
    #asign the rest
    streamFunction[isNotBoundaryNode]=reducedSF[len(boundaryNodes):]
    return streamFunction

def updateMeshCurrentDensityFaces(mesh,optStreamFkt):
    '''updates the current density of the Faces in the mesh'''
    pot1 = np.transpose(np.array([optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,0]],optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,0]],optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,0]]]))
    pot2 = np.transpose(np.array([optStreamFkt[mesh.faces[:,1]]-optStreamFkt[mesh.faces[:,0]],optStreamFkt[mesh.faces[:,1]]-optStreamFkt[mesh.faces[:,0]],optStreamFkt[mesh.faces[:,1]]-optStreamFkt[mesh.faces[:,0]]]))
    pot3 = np.transpose(np.array([optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,1]],optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,1]],optStreamFkt[mesh.faces[:,2]]-optStreamFkt[mesh.faces[:,1]]]))
    edge1 = mesh.vertices[mesh.faces[:,2]]-mesh.vertices[mesh.faces[:,0]]
    edge2 = mesh.vertices[mesh.faces[:,1]]-mesh.vertices[mesh.faces[:,0]]
    edge3 = mesh.vertices[mesh.faces[:,2]]-mesh.vertices[mesh.faces[:,1]]
    mesh.currentDensityFaces = edge1*pot1+edge2*pot2+edge3*pot3

def reduceMatricesForBoundaryNodesTest():
    matToRed = [[0.00000000e+00, 1.74378494e-05, 0.00000000e+00, 1.12500000e-05,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.12500000e-05,
    0.00000000e+00 ,0.00000000e+00],
    [1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05, 0.00000000e+00,
    1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 1.74378494e-05,
    1.74378494e-05 ,0.00000000e+00],
    [0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,6.18784938e-06 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,6.18784938e-06],
    [1.12500000e-05 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.12500000e-05, 1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00, 0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,1.74378494e-05 ,6.18784938e-06 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    6.18784938e-06 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.12500000e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.12500000e-05 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,6.18784938e-06 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,6.18784938e-06,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.12500000e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.12500000e-05 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    6.18784938e-06 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,6.18784938e-06 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.12500000e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.12500000e-05,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,6.18784938e-06,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,6.18784938e-06 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.12500000e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.12500000e-05 ,1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,6.18784938e-06 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    6.18784938e-06 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.12500000e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.12500000e-05 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,6.18784938e-06 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,6.18784938e-06,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.12500000e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.12500000e-05 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05,
    6.18784938e-06 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,6.18784938e-06 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.12500000e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,1.12500000e-05,
    1.74378494e-05 ,0.00000000e+00],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00,
    1.74378494e-05 ,1.74378494e-05],
    [0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,1.74378494e-05 ,6.18784938e-06,
    0.00000000e+00 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,6.18784938e-06],
    [1.12500000e-05 ,1.74378494e-05 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.12500000e-05 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00],
    [0.00000000e+00 ,1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    1.74378494e-05 ,1.74378494e-05 ,0.00000000e+00 ,1.74378494e-05,
    0.00000000e+00 ,1.74378494e-05],
    [0.00000000e+00 ,0.00000000e+00 ,6.18784938e-06 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00 ,0.00000000e+00,
    0.00000000e+00 ,1.74378494e-05 ,6.18784938e-06 ,0.00000000e+00,
    1.74378494e-05 ,0.00000000e+00]]
    meshBoundaries = [[2, 5, 8, 11, 14, 17, 20, 23, 26, 29], [1, 3, 6, 9, 12, 15, 18, 21, 24, 27]]
    meshVertices = [[ 3.00000000e+00,  0.00000000e+00 ,-2.50000000e+00],
    [ 3.00000000e+00,  0.00000000e+00,  0.00000000e+00],
    [ 3.00000000e+00,  0.00000000e+00,  2.50000000e+00],
    [ 2.42705098e+00,  1.76335576e+00, -2.50000000e+00],
    [ 2.42705098e+00,  1.76335576e+00,  0.00000000e+00],
    [ 2.42705098e+00,  1.76335576e+00,  2.50000000e+00],
    [ 9.27050983e-01,  2.85316955e+00, -2.50000000e+00],
    [ 9.27050983e-01,  2.85316955e+00,  0.00000000e+00],
    [ 9.27050983e-01,  2.85316955e+00,  2.50000000e+00],
    [-9.27050983e-01,  2.85316955e+00, -2.50000000e+00],
    [-9.27050983e-01,  2.85316955e+00,  0.00000000e+00],
    [-9.27050983e-01,  2.85316955e+00,  2.50000000e+00],
    [-2.42705098e+00,  1.76335576e+00, -2.50000000e+00],
    [-2.42705098e+00,  1.76335576e+00,  0.00000000e+00],
    [-2.42705098e+00,  1.76335576e+00,  2.50000000e+00],
    [-3.00000000e+00,  3.67394040e-16, -2.50000000e+00],
    [-3.00000000e+00,  3.67394040e-16,  0.00000000e+00],
    [-3.00000000e+00,  3.67394040e-16,  2.50000000e+00],
    [-2.42705098e+00, -1.76335576e+00, -2.50000000e+00],
    [-2.42705098e+00, -1.76335576e+00,  0.00000000e+00],
    [-2.42705098e+00, -1.76335576e+00,  2.50000000e+00],
    [-9.27050983e-01, -2.85316955e+00, -2.50000000e+00],
    [-9.27050983e-01, -2.85316955e+00,  0.00000000e+00],
    [-9.27050983e-01, -2.85316955e+00,  2.50000000e+00],
    [ 9.27050983e-01, -2.85316955e+00, -2.50000000e+00],
    [ 9.27050983e-01, -2.85316955e+00,  0.00000000e+00],
    [ 9.27050983e-01, -2.85316955e+00,  2.50000000e+00],
    [ 2.42705098e+00, -1.76335576e+00, -2.50000000e+00],
    [ 2.42705098e+00, -1.76335576e+00,  0.00000000e+00],
    [ 2.42705098e+00, -1.76335576e+00,  2.50000000e+00]]
    meshVertices = np.transpose(meshVertices)
    zeroFlag = False
    return reduceMatricesForBoundaryNodes(matToRed,meshVertices,meshBoundaries,zeroFlag) == [[[3.48756988e-04, 3.48756988e-04, 3.48756988e-05, 3.48756988e-05,
        3.48756988e-05, 3.48756988e-05, 3.48756988e-05, 3.48756988e-05,
        3.48756988e-05, 3.48756988e-05, 3.48756988e-05, 3.48756988e-05],
       [3.48756988e-04, 9.90055901e-05, 1.12500000e-05, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 1.12500000e-05, 1.23756988e-05],
       [3.48756988e-05, 1.12500000e-05, 0.00000000e+00, 1.12500000e-05,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 1.12500000e-05, 0.00000000e+00,
        1.12500000e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 1.12500000e-05,
        0.00000000e+00, 1.12500000e-05, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        1.12500000e-05, 0.00000000e+00, 1.12500000e-05, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 1.12500000e-05, 0.00000000e+00, 1.12500000e-05,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 1.12500000e-05, 0.00000000e+00,
        1.12500000e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.12500000e-05,
        0.00000000e+00, 1.12500000e-05, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        1.12500000e-05, 0.00000000e+00, 1.12500000e-05, 0.00000000e+00],
       [3.48756988e-05, 1.12500000e-05, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 1.12500000e-05, 0.00000000e+00, 0.00000000e+00],
       [3.48756988e-05, 1.23756988e-05, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]], [[2, 5, 8, 11, 14, 17, 20, 23, 26, 29], [1, 3, 6, 9, 12, 15, 18, 21, 24, 27]], [0, 4, 7, 10, 13, 16, 19, 22, 25, 28]]