import numpy as np
import matplotlib.pyplot as plt
import meshzoo
import trimesh

def calculateNormal(vec):
    '''returns the norm for a given 3d vector'''
    if len(vec) == 3:
        v1 = vec[1] - vec[0]
        v2 = vec[2] - vec[0]
        return np.cross(v1,v2)/np.sqrt(np.cross(v1,v2)[0]**2+np.cross(v1,v2)[1]**2+np.cross(v1,v2)[2]**2)
    else:
        print("Mesh-Generation is going wrong. Faces do not have 3 components")
        return False

def updateList(edgeList,otheredge):
    '''returns the edgeList without otheredge'''
    return [a for a, skip in zip(edgeList, [np.allclose(a, otheredge) for a in edgeList]) if not skip]

#option 1: create mesh
class CylindricMesh():
    def __init__(self, coilLength, coilRadius, n):
        self.vertices, self.faces = meshzoo.tube(length=coilLength, radius=coilRadius, n=int(n)) # points, cells(index of the points that close the cell)
        self.vertices = np.array(self.vertices)
        self.normals=self.getNormals()
        self.openBoundaries=self.getOpenBoundaries()
        self.areas = self.getAreas()
        self.current = self.getCurrent()
        self.neighbours=self.getNeighbourTriangleIndices()
        self.rotatedCaylinder=self.getRotatedCopy()
        self.u,self.v=self.get2Dcoordinates()
        self.neighbourareas = self.getNeighbourAreas()
        self.currentDensityFaces=[]
        self.vertexNormals=self.getVertexNormals()
        self.boundary = self.checkIfBoundary()
        self.oneRingList = self.getOneRingList()
        self.neighbourcurrents = self.getNeighbourCurrents()
        self.neighbourcurrentUnsorted = self.getNeighbourCurrentsUnsorted()

    def checkIfBoundary(self):
        '''returns a list of boolean if the vertice is a boundary vertice'''
        boundaryBooleans = []
        for nodeElements in range(len(self.vertices)):
            boundaryBooleans.append((nodeElements in self.openBoundaries[0]) | (nodeElements in self.openBoundaries[1]))
        return boundaryBooleans

    def getVertexNormals(self):
        '''returns the normals of the vertices. These are calculated as average of the touching faces normals.'''
        vertexNormals = []
        for vertex in range(len(self.vertices)):
            sum = 0
            for x in np.array(self.neighbours[vertex]):
                sum+= self.normals[x]
            vertexNormals.append(sum/len(self.neighbours[vertex]))
        return vertexNormals

    def getNormals(self):
        '''returns the normals of the faces'''
        normals=[]
        for i in range(len(self.faces)):
            normals.append(calculateNormal(self.vertices[self.faces[i]]))
        return normals

    def getNeighbourAreas(self):
        '''returns the areas of the neighbour triangles for every node'''
        neighbourareas = []
        for i in range(len(self.vertices)):
            neighbourareasparts=[]
            for j in self.neighbours[i]:
                neighbourareasparts.append(self.areas[j])
            neighbourareas.append(neighbourareasparts)
        return neighbourareas

    def getNeighbourCurrents(self):
        '''returns the currents of the neighbour triangles for every node'''
        neighbourcurrents = []
        for i in range(len(self.vertices)):
            neighbourcurrentparts=[]
            for j in self.oneRingList[i]:
                neighbourcurrentparts.append((self.vertices[j[1]] - self.vertices[j[0]]) \
                    / np.linalg.norm(np.cross(self.vertices[j[1]]-self.vertices[i],self.vertices[j[0]] - self.vertices[i])))
            neighbourcurrents.append(neighbourcurrentparts)
        return neighbourcurrents

    def getNeighbourCurrentsUnsorted(self):
        '''returns the currents of the neighbour triangles for every node before sorting'''
        neighbourcurrents = []
        for i in range(len(self.vertices)):
            neighbourcurrentparts=[]
            for j in self.neighbours[i]:
                neighbourcurrentparts.append(self.current[j])
            neighbourcurrents.append(neighbourcurrentparts)
        return neighbourcurrents

    def getCurrent(self):
        '''returns the current for the triangles made with the points in faces
        C = (c-b)/(2*Fläche)'''
        current =[]
        for i in range(len(self.areas)):
            current.append((self.vertices[self.faces[i][2]]-self.vertices[self.faces[i][1]])/(2*self.areas[i]))
        return current

    def getAreas(self):
        '''returns the areas of the triangles made with the points in faces'''
        areas=[]
        for i in self.faces:
            areas.append(np.linalg.norm(np.cross((self.vertices[i[1]] - self.vertices[i[0]]),
                (self.vertices[i[2]] - self.vertices[i[0]])))/2)
        return areas

    def getOpenBoundaries(self):
        '''returns indexes of the nodes at the edges of a cylinder extended in z-direction'''
        max = 0
        upperopen=[]
        min = 0
        loweropen=[]
        for i in range(len(self.vertices)):
            if self.vertices[i][2]< min:
                min = self.vertices[i][2]
                loweropen = [i]
            elif self.vertices[i][2] == min:
                loweropen.append(i)
            elif self.vertices[i][2]>max:
                max = self.vertices[i][2]
                upperopen = [i]
            elif self.vertices[i][2]==max:
                upperopen.append(i)
            else: continue
        return [upperopen,loweropen]#TODO tauschen

    def getBoundaryEdges(self):
        '''returns the nodes for each boundary in the correct order'''
        boundaryEdges=[]
        for boundary in self.openBoundaries:
            eachBoundaryEdges=[]
            for boundaryPoint in boundary:
                for neighbour in self.faces[self.neighbours[boundaryPoint]]:
                    for neighbournode in neighbour:
                        if neighbournode in boundary and neighbournode != boundaryPoint:
                                eachBoundaryEdges.append([boundaryPoint,neighbournode])
            eachBoundaryEdges = self.removeDoubleEdges(eachBoundaryEdges)
            boundaryEdges.append(eachBoundaryEdges)
        return boundaryEdges

    def removeDoubleEdges(self,edgeList):
        '''returns the edgeList with each edge just once.'''
        newList=np.copy(edgeList)
        for edgeInd in range(len(newList)):
            for otheredgeInd in range(len(newList)):
                if (newList[edgeInd][::-1] == newList[otheredgeInd]).all() and edgeInd < otheredgeInd:
                    edgeList = updateList(edgeList,newList[otheredgeInd])
        return edgeList

    def getBoundaryLoopNodes(self):
        '''returns the unsorted nodes for the boundaryLoop.'''
        boundaryEdges = self.getBoundaryEdges()
        boundaryEdges = self.turnAnsSortElements(boundaryEdges)
        boundaryEdges = [np.flip(boundaryEdges[1]),boundaryEdges[0]] #TODO welche Regelmäßigkeit, warum so?
        boundaryLoopNodes=[]
        for boundary in boundaryEdges:
            boundaryNodes = np.append(np.array(boundary)[:,0],boundary[0][0])
            boundaryLoopNodes.append(boundaryNodes)
        return boundaryLoopNodes

    def getRotatedCopy(self):
        '''returns rotated copy of the vertices. If the cylinder is orientated along the z axis we need a rotated copy.'''
        boundaryLoopNodes = self.getBoundaryLoopNodes()
        rotationVec,angle = self.calcRotationVec(boundaryLoopNodes)
        rotMat = self.calc3DRotMatByVec(rotationVec,angle)
        rotatedVertices = self.getRotatedVertices(rotMat)
        return rotatedVertices

    def getRotatedVertices(self,rotMat):
        '''returns the rotated vertices (multiplication with rotMat).'''
        rotatedVertices = []
        for i in self.vertices:
            rotatedVertices.append(np.dot(rotMat,np.transpose(i)))
        return rotatedVertices

    def calcRotationVec(self,boundaryLoopNodes):
        '''returns the rotationVector and the angle based on the boundaryLoopNodes.'''
        openingMean = [np.mean(self.vertices[boundaryLoopNodes[0]][:,0]),
            np.mean(self.vertices[boundaryLoopNodes[0]][:,1]), np.mean(self.vertices[boundaryLoopNodes[0]][:,2])]
        overallMean = np.mean(self.vertices)
        oldOrientationVec=(openingMean-overallMean)/np.linalg.norm(openingMean-overallMean)
        zVec = [0,0,1]
        sina = np.linalg.norm(np.cross(oldOrientationVec,zVec))/(np.linalg.norm(oldOrientationVec)*np.linalg.norm(zVec))
        cosa = np.linalg.norm(np.dot(oldOrientationVec,zVec))/(np.linalg.norm(oldOrientationVec)*np.linalg.norm(zVec))
        angle = np.arctan2(sina,cosa)
        rotationVec = np.cross(oldOrientationVec,zVec)/np.linalg.norm(np.cross(oldOrientationVec,zVec))
        return rotationVec,angle

    def calc3DRotMatByVec(self,rotationVec,angle):
        '''returns the rotation matrix calculated from the rotationVector'''
        uX,uY,uZ = rotationVec
        tmp1 = np.sin(angle)
        tmp2 = np.cos(angle)
        tmp3 = (1-np.cos(angle))
        rotMat = np.zeros((3,3))
        rotMat[0][0] = tmp2 + uX*uX*tmp3
        rotMat[0][1] = uX*uY*tmp3-uZ*tmp1
        rotMat[0][2] = uX*uZ*tmp3+uY*tmp1
        rotMat[1][0] = uY*uX*tmp3+uZ*tmp1
        rotMat[1][1] = tmp2+uY*uY*tmp3
        rotMat[1][2] = uY*uZ*tmp3-uX*tmp1
        rotMat[2][0] = uZ*uX*tmp3-uY*tmp1
        rotMat[2][1] = uZ*uX*tmp3+uX*tmp1
        rotMat[2][2] = tmp2+uZ*uZ*tmp3
        return rotMat

    def turnAnsSortElements(self,boundaryEdges):
        '''returns the given list in sorted. If needed single elements were turned to close the loop.'''
        new=[]
        for boundary in boundaryEdges:
            start = boundary[0]
            newElement = [start]
            while len(newElement) < len(boundary):
                for element in boundary:
                    if start == element:
                        continue
                    elif start[1] == element[0]:
                        if element[1] is not start[0]:
                            newElement.append(element)
                            break
                    elif start[1] == element[1]:
                        if start[0] is not element[1]:
                            newElement.append([element[1],element[0]])
                            break
                start = newElement[-1]
            new.append(newElement)
        return new

    def get2Dcoordinates(self):
        '''returns the from 3D to 2D converted vertices'''
        corods = np.array(self.rotatedCaylinder)
        minZCylinder = min(corods[:,2])
        corods[:,2] = corods[:,2]+minZCylinder
        phiCoord = np.arctan2(corods[:,1],corods[:,0])
        r = np.sqrt(corods[:,0]**2+corods[:,1]**2)
        u = (corods[:,2]-np.mean(r))*np.sin(phiCoord)
        v = (corods[:,2]- np.mean(r))*np.cos(phiCoord)
        return u,v

    def getNeighbourTriangleIndices(self):
        '''returns the indices of the neighbour triangles of every node'''
        neighbourtrianglesIndices=[] 
        for node in self.vertices:
            k=[]
            for i in range(len(self.faces)):
                vecList = self.vertices[self.faces[i]]
                if checkIfVecInVeclist(node,vecList):
                    k.append(i)
            neighbourtrianglesIndices.append(k)
        return neighbourtrianglesIndices

    def getOneRingList(self):
        '''returns sorted list with nodes around every node'''
        oneRingList = self.createOneRingList()
        oneRingList = self.ensureUniformOrientation(oneRingList)
        oneRingList = self.orderElementsInCircularArangement(oneRingList)
        return oneRingList

    def orderElementsInCircularArangement(self, oneRingList):
        '''returns the List in a circular arrangement'''
        for nodeId in range(len(oneRingList)):
            if self.boundary[nodeId]:
                startIdx = self.findStartInBoundaryCase(oneRingList,nodeId)
            else:
                startIdx = 0

            newIdcs = self.arrangeCircular(startIdx, oneRingList[nodeId])
            oneRingList[nodeId] = list(oneRingList[nodeId][i] for i in newIdcs)
            # neighbours also needs to be reordered, because it is indexed by triangleId !
            self.neighbours[nodeId] = list(self.neighbours[nodeId][i] for i in newIdcs)
        return oneRingList

    def arrangeCircular(self, startIdx, ringListItem):
        '''returns the elements in a circular order beginning with start'''
        newIdcs = [startIdx]
        while len(newIdcs) != len(ringListItem):
            for i in range(len(ringListItem)):
                if len(newIdcs) == len(ringListItem):
                    break
                if ringListItem[newIdcs[-1]][1] == ringListItem[i][0]:
                    newIdcs.append(i)
        return newIdcs

    def findStartInBoundaryCase(self, oneRingList, nodeNumber):
        '''returns the correct start triangle for ordering the triangles around a boundary vertice'''
        index = 0
        start = oneRingList[nodeNumber][0] 
        correctstart = self.checkStartTriangle(oneRingList[nodeNumber],start)
        while not correctstart:
            start = oneRingList[nodeNumber][index+1]
            correctstart = self.checkStartTriangle(oneRingList[nodeNumber],start)
            index+=1
        return index

    def checkStartTriangle(self,verticeTriangles,start):
        '''returns boolean if "start" is the correct startTriangle'''
        test = []
        for i in range(len(verticeTriangles)):
            test.append(start[0]==verticeTriangles[i][1])
        return not np.any(test)

    def createOneRingList(self):
        '''returns a list with the other two triangle Points for each triangle per node'''
        indices = self.getNeighbourTriangleIndices()
        oneRingList=[]
        for i in range(len(indices)):
            eachnode=[]
            for k in range(len(indices[i])):
                new=[]
                for j in range(3):
                    if self.faces[indices[i][k]][j] != i:
                        new.append(self.faces[indices[i][k]][j])
                eachnode.append(new)
            oneRingList.append(eachnode)
        return oneRingList

    def ensureUniformOrientation(self,oneRingList):
        '''returns oneRingList with ensured uniform Orientation'''
        for nodeelements in range(len(oneRingList)):
            for neighbournodes in oneRingList[nodeelements]:
                b = self.vertices[neighbournodes[0]]
                c = self.vertices[neighbournodes[1]]
                a = self.vertices[nodeelements]
                crossVec = np.cross(c-b,b-a)

                if np.sign(np.dot(self.vertexNormals[nodeelements],crossVec)) > 0:
                    before0 = neighbournodes[0]
                    before1 = neighbournodes[1]
                    neighbournodes[0] = before1
                    neighbournodes[1] = before0
        return oneRingList


#option 2: create cylindric mesh
def getMeshFromSTL(filename):
    '''returns vertices and faces from given stl file meshes'''
    myobj = trimesh.load_mesh(filename, enable_post_processing=True, solid=True)
    return myobj.vertices, myobj.faces

class CylindricMeshGiven(CylindricMesh):
    def __init__(self,filename):
        self.vertices,self.faces = getMeshFromSTL(filename)
        self.vertices = np.array(self.vertices)
        self.normals=self.getNormals()
        self.openBoundaries=self.getOpenBoundaries()
        self.areas = self.getAreas()
        self.current = self.getCurrent()
        self.neighbours=self.getNeighbourTriangleIndices()
        self.rotatedCaylinder=self.getRotatedCopy()
        self.u,self.v=self.get2Dcoordinates()
        self.neighbourareas = self.getNeighbourAreas()
        self.currentDensityFaces=[]
        self.vertexNormals=self.getVertexNormals()
        self.boundary = self.checkIfBoundary()
        self.oneRingList = self.getOneRingList()
        self.neighbourcurrents = self.getNeighbourCurrents()
        self.neighbourcurrentUnsorted = self.getNeighbourCurrentsUnsorted()

def checkIfVecInVeclist(node,vecList):
    '''returns Boolean if a 3 components vec is in a list of 3 component elements'''
    return (node == vecList[0]).all()|(node == vecList[1]).all()|( node == vecList[2]).all()




## Testing ##
# createdmesh = CylindricMesh(5.0,3.0,10)
#givenMesh = CylindricMeshGiven('C:\\Users\Simone\git\Py-CoilGen\cylinder_radius500mm_length1500mm.stl')

#x,y = mesh.get2Dcoordinates()
#plt.plot(x,y,'.')
#plt.show()


### optische Mesh Kontrolle - nur zur Veranschaulichung
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# X=[]
# Y=[]
# Z=[]
# print(np.shape(mesh.vertices))
# for i in range(len(mesh.vertices)):
#     X.append(mesh.vertices[i][0])
#     Y.append(mesh.vertices[i][1])
#     Z.append(mesh.vertices[i][2])
# ax.scatter3D(X,Y,Z)
# plt.show()

