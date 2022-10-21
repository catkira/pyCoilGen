#Flächenströme der Dreieck um jeden Knoten aufintegrieren
from itertools import zip_longest
import numpy as np
import scipy

def getSensitivityMatrix(test,mesh,target,n):
    '''returns the sensitivity Matrix for the mesh'''
    biotSavatCoeff = 10**(-7)
    sensitivityMatrix = []
    [u,v,gaussWeight] = gaussLegendreIntegrationPointsTriangle(n)
    test.gaußLegendre = [u,v,gaussWeight]
    trianglesPerNode=[]
    trianglesPerNode.append([len(mesh.neighbours[x]) for x in range(len(mesh.neighbours))])
    trianglesPerNode = trianglesPerNode[0]
    xTarget,yTarget,zTarget = target.vertices[:,0],target.vertices[:,1],target.vertices[:,2]
    xAll,yAll,zAll=[],[],[]
    for nodeIndex in range(len(mesh.vertices)):
        dCx,dCy,dCz = np.zeros(len(xTarget)),np.zeros(len(xTarget)),np.zeros(len(xTarget))
        for triangleIndex in range(trianglesPerNode[nodeIndex]):
            nodePoint = mesh.vertices[nodeIndex]
            pointB = mesh.vertices[mesh.oneRingList[nodeIndex][triangleIndex][0]]
            pointC = mesh.vertices[mesh.oneRingList[nodeIndex][triangleIndex][1]]
            nodeX,nodeY,nodeZ = nodePoint
            bX,bY,bZ = pointB
            cX,cY,cZ = pointC
            vX,vY,vZ = (pointC - pointB)/(scipy.linalg.norm(np.cross(pointC-nodePoint,pointB-nodePoint)))
            for gaussIndex in range(len(gaussWeight)):
                xGaussInUV = nodeX*u[gaussIndex]+bX*v[gaussIndex]+cX*(1-u[gaussIndex]-v[gaussIndex])#scalar
                yGaussInUV = nodeY*u[gaussIndex]+bY*v[gaussIndex]+cY*(1-u[gaussIndex]-v[gaussIndex])#scalar
                zGaussInUV = nodeZ*u[gaussIndex]+bZ*v[gaussIndex]+cZ*(1-u[gaussIndex]-v[gaussIndex])#scalar
                distanceNorm = (np.square(xGaussInUV-xTarget)+np.square(yGaussInUV-yTarget)+np.square(zGaussInUV-zTarget))**(-3/2)#for biot savat #len of target
                dCx = dCx + ((-1)*vZ*(yTarget-yGaussInUV)+ vY*(zTarget-zGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
                dCy = dCy + ((-1)*vX*(zTarget-zGaussInUV)+ vZ*(xTarget-xGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
                dCz = dCz + ((-1)*vY*(xTarget-xGaussInUV)+ vX*(yTarget-yGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
          
        dCx *= biotSavatCoeff
        dCy *= biotSavatCoeff
        dCz *= biotSavatCoeff
        xAll.append(dCx)
        yAll.append(dCy)
        zAll.append(dCz)
    xAll = xAll
    yAll = yAll
    zAll = zAll
    sensitivityMatrix=[xAll,yAll,zAll]   
    return sensitivityMatrix

def gaussLegendreIntegrationPointsTriangle(n):
    '''returns the weights and the test point for the gauss legendre'''
    u,v,ck=[],[],[]
    eta,w = calcWeightsGauss(n)
    for i in range(len(eta)):
        for j in range(len(eta)):
            u.append((1+eta[i])/2)
            v.append((1-eta[i])*(1+eta[j])/4)
            ck.append(((1-eta[i])/8)*w[i]*w[j])
    return [u,v,ck]

def calcWeightsGauss(n):
    '''returns the abscissa and the weights for a Gauss-Legendre quadrature'''
    abscissa = np.zeros(n)
    weights = np.copy(abscissa)
    m = (n+1)/2
    for i in np.arange(1,m).reshape(-1):
        z = np.cos(np.pi*(i-0.25)/(n+0.5))
        z1 = z+1
        while abs(z-z1)>(2.2204*10**(-16)):#distance from 1.0 to the next larger double precision number
            p1 = 1
            p2 = 0
            for j in range(n):
                p3 = np.copy(p2)
                p2 = np.copy(p1)
                p1 = ((2*(j+1)-1)*z*p2-((j+1)-1)*p3)/(j+1)
            pp = n*(z*p1-p2)/(z**2-1)
            z1 = np.copy(z)
            z = z1-p1/pp
        abscissa[int(i-1)] = -z
        abscissa[int(n+1-i-1)] = z
        weights[int(i-1)] = 2/((1-z**2)*pp**2)
        weights[int(n+1-i-1)] = weights[int(i-1)]
    return abscissa,weights
