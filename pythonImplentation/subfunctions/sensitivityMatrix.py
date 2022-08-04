#Flächenströme der Dreieck um jeden Knoten aufintegrieren
import numpy as np

def getSensitivityMatrix(mesh,target,n):
    biotSavatCoeff = 10**(-7)
    sensitivityMatrix = []
    [u,v,gaussWeight] = gaussLegendreIntegrationPointsTriangle(n)
    trianglesPerNode = [len(mesh.neighbours[x]) for x in range(len(mesh.neighbours))]
    xTarget,yTarget,zTarget = splitListColumns(target.vertices)
    for nodeIndex in range(len(mesh.vertices)):
        dCx,dCy,dCz =[0,0,0],[0,0,0],[0,0,0]
        for triangleIndex in range(trianglesPerNode[nodeIndex]):
            nodePoint = mesh.faces[mesh.neighbours[nodeIndex][triangleIndex]][0]
            pointB = mesh.faces[mesh.neighbours[nodeIndex][triangleIndex]][1]
            pointC = mesh.faces[mesh.neighbours[nodeIndex][triangleIndex]][2]
            nodeX = mesh.vertices[nodePoint][0]
            nodeY = mesh.vertices[nodePoint][1]
            nodeZ = mesh.vertices[nodePoint][2]
            bX = mesh.vertices[pointB][0]
            bY = mesh.vertices[pointB][1]
            bZ = mesh.vertices[pointB][2]
            cX = mesh.vertices[pointC][0]
            cY = mesh.vertices[pointC][1]
            cZ = mesh.vertices[pointC][2]
            vX = mesh.current[mesh.neighbours[nodeIndex][triangleIndex]][0]
            vY = mesh.current[mesh.neighbours[nodeIndex][triangleIndex]][1]
            vZ = mesh.current[mesh.neighbours[nodeIndex][triangleIndex]][2]

            for gaussIndex in range(len(gaussWeight)):
                xGaussInUV = nodeX*u[gaussIndex]+bX*v[gaussIndex]+cX*(1-u[gaussIndex]-v[gaussIndex])
                yGaussInUV = nodeY*u[gaussIndex]+bY*v[gaussIndex]+cY*(1-u[gaussIndex]-v[gaussIndex])
                zGaussInUV = nodeZ*u[gaussIndex]+bZ*v[gaussIndex]+cZ*(1-u[gaussIndex]-v[gaussIndex])
                distanceNorm = (np.square(xGaussInUV-xTarget)+np.square(yGaussInUV-yTarget)+np.square(zGaussInUV-zTarget))**(-3/2)#for biot savat
                dCx = dCx + ((-1)*vZ*(yTarget-yGaussInUV)+ vY*(zTarget-zGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
                dCy = dCy + ((-1)*vX*(zTarget-zGaussInUV)+ vZ*(xTarget-xGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
                dCz = dCz + ((-1)*vY*(xTarget-xGaussInUV)+ vX*(yTarget-yGaussInUV))*distanceNorm *2 *mesh.areas[mesh.neighbours[nodeIndex][triangleIndex]]* gaussWeight[gaussIndex]
                #beitrag zur sensitivitätsmatrix dCx,dCy,dCz
            dCx *= biotSavatCoeff
            dCy *= biotSavatCoeff
            dCz *= biotSavatCoeff
        sensitivityMatrix.append([dCx,dCy,dCz])
        #print(sensitivityMatrix) #achtung viel output!
    return sensitivityMatrix

def splitListColumns(mehrDimList):#WIP allgemeiner schreiben
    xTarget=[]
    yTarget=[]
    zTarget=[]
    for i in range(len(mehrDimList)):
        xTarget.append(mehrDimList[i][0])
        yTarget.append(mehrDimList[i][1])
        zTarget.append(mehrDimList[i][2])
    return xTarget,yTarget,zTarget


def gaussLegendreIntegrationPointsTriangle(n):
    u,v,ck=[],[],[]
    eta,w = calcWeightsGauss(n)
    for i in range(len(eta)):
        for j in range(len(eta)):
            u.append((1+eta[i])/2)
            v.append((1-eta[i])*(1+eta[j]))
            ck.append(((1-eta[i])/8)*w[i]*w[j])
    return [u,v,ck]


def calcWeightsGauss(n):
    #n = n-1 #anpassung matlab n -> python n-1 (index start 1 bzw 0) NOCH NICHT IM VERGLEICH GETESTET !! 
    abscissa = np.zeros(n+1)
    weights = abscissa
    m = (n+1)/2
    for i in np.arange(1,m).reshape(-1):
        z = np.cos(np.pi*(i-0.25)/(n+0.5))
        z1 = z+1
    while abs(z-z1)>(2.2204*10**(-16)):#distance from 1.0 to the next larger double precision number
        p1 = 1
        p2 = 0
        for j in np.arange(1,n).reshape(-1):
            p3 = p2
            p2 = p1
            p1 = ((2*j-1)*z*p2-(j-1)*p3)/j
        pp = n*(z*p1-p2)/(z**2-1)
        z1 = z
        z = z1-p1/pp
    abscissa[int(i)] = -z
    abscissa[int(n+1-i)] = z
    weights[int(i)] = 2/((1-z**2)*pp**2)
    weights[int(n+1-i)] = weights[int(i)]
    return abscissa,weights
