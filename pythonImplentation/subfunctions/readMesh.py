# we need mesh, vertices and faces from the mesh
import numpy as np
import matplotlib.pyplot as plt
import meshzoo
from stl import mesh
import trimesh


#option 1: given mesh 
class CylindricMesh():
    def __init__(self,coilLength,coilRadius,n):
        self.vertices, self.faces = meshzoo.tube(length=coilLength, radius=coilRadius, n=int(n))#points, cells(index of the points that close the cell)
        self.normals=self.getNormals
        self.openBoundaries=self.getOpenBoundaries()
        self.u,self.v=self.get2Dcoordinates()
        self.areas = self.getAreas()
        self.current = self.getCurrent()
        self.neighbours=self.getNeighbourTriangleIndices()#WIP nicht sortiert ...#we want a list of the triangles/faces aroud the node instead
        self.neighbourcurrents = self.getNeighbourCurrents()
        self.neighbourareas = self.getNeighbourAreas()
        self.currentDensityFaces=[]

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
            areas.append(np.linalg.norm(np.cross((self.vertices[i[1]]-self.vertices[i[0]]),(self.vertices[i[2]]-self.vertices[i[0]]))))
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
        return [upperopen,loweropen]

    #bei z +1 statt wie bei philipp -zmin
    def get2Dcoordinates(self):
        '''returns the from 3D to 2D converted vertices'''
        u=[]
        v=[]
        for i in range(len(self.vertices)):
            r = np.sqrt(self.vertices[i][0]**2+self.vertices[i][1]**2)
            u.append((r-self.vertices[i][2]+1)*np.sin(np.arctan2(self.vertices[i][0],self.vertices[i][1])))
            v.append((r-self.vertices[i][2]+1)*np.cos(np.arctan2(self.vertices[i][0],self.vertices[i][1])))
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
            
#option 2: create cylindric mesh 
def getMesh(filename):
    myobj = trimesh.load_mesh(filename, enable_post_processing=True, solid=True)
    return myobj.vertices, myobj.faces

class CylindricMeshGiven(CylindricMesh):
    def __init__(self,filename):
        self.vertices,self.faces = getMesh(filename)
        self.normals=self.getNormals
        self.openBoundaries=self.getOpenBoundaries()
        self.u,self.v=self.get2Dcoordinates()
        self.areas = self.getAreas()
        self.current = self.getCurrent()
        self.neighbours=self.getNeighbourTriangleIndices()#WIP nicht sortiert ...#we want a list of the triangles/faces aroud the node instead
        self.neighbourcurrents = self.getNeighbourCurrents()
        self.neighbourareas = self.getNeighbourAreas()
        self.currentDensityFaces=[]
    
def checkIfVecInVeclist(node,vecList):
    '''returns Boolean if a 3 components vec is in a list of 3 component elements'''
    return (node == vecList[0]).all()|(node == vecList[1]).all()|( node == vecList[2]).all()



createdmesh = CylindricMesh(5.0,3.0,10)
givenMesh = CylindricMeshGiven('cylinder_radius500mm_length1500mm.stl')
print("given mesh",np.shape(givenMesh.vertices))
print("created mesh",np.shape(createdmesh.vertices))






def correctList(old):
    '''ensures that each element appears only once in the list'''
    new=[]
    for i in old:
        if i in new:
            continue
        else:
            new.append(i)
    return new


#TODO test function for normals (nach außen und alle gleich!)

def test_EqualDirectionsNormal(mesh): #WIP
    for i in range(len(mesh.faces)):
        print("Normle Dreieck Nummer ",i, "ist" , calculateNormal(mesh.vertices[mesh.faces[i]]))

def test_IfLonelyVertice(mesh):
    for i in range(len(mesh.vertices)):
        if(any(i in sublist for sublist in mesh.faces)):
             continue
        else:print("LONELY POINT: ", i)   
    print("finished test")


def calculateNormal(vec):
    if len(vec) == 3:
        v1 = vec[1] - vec[0]
        v2 = vec[2] - vec[0]
        return np.cross(v1,v2)
    else:
        #Fall das faces nicht aus 3 Komponenten besteht im Kopf behalten, evtl bei direkter Mesh Einspeisung handeln. (create_unique_noded_mesh)
        print("Mesh-Generation is going wrong. Faces do not have 3 components")
        return False

#test_EqualDirectionsNormal(mesh)
#test_IfLonelyVertice(mesh)
#print(mesh.openBoundaries)
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

