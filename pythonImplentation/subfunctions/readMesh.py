# we need mesh, vertices and faces from the mesh

#option 1: given mesh 
#option 2: create cylindric mesh 
import numpy as np
import matplotlib.pyplot as plt
import meshzoo

class CylindricMesh():
    def __init__(self,coilLength,coilRadius,n):
        self.vertices, self.faces = meshzoo.tube(length=coilLength, radius=coilRadius, n=int(n))#points, cells(index of the points that close the cell)
        self.normals=self.getNormals
        self.openBoundaries=self.getOpenBoundaries()
        self.u,self.v=self.get2Dcoordinates()
        self.neighbours=self.getNeighbourTriangleIndices()#WIP nicht sortiert ...#we want a list of the triangles/faces aroud the node instead
        self.areas = self.getAreas()
        self.current = self.getCurrent()
        self.test = self.getSuroundingTriangles()

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

    def getNormals(self):
        '''returns the normals of the faces'''
        normals=[]
        for i in range(len(self.faces)):
            normals.append(calculateNormal(self, self.faces[i]))
        return normals
    
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
        #faces abrastern und je die andern beiden Punkte in liste schreiben (mit index)
        #WIP dirty fix
        neighbourtrianglesIndices=[]
        for node in self.vertices:
            k=[]
            for i in range(len(self.faces)):
                if node in self.faces[i]:
                    k.append(i)
            neighbourtrianglesIndices.append(k)
        # neighbours=[]
        # for i in range(len(self.vertices)):
        #     neighboursThis=[]
        #     for j in self.faces:
        #         if i in j:
        #             for k in range(3):
        #                 if i == j[k]:
        #                     continue
        #                 else: neighboursThis.append(j[k])
        #     neighbours.append(correctList(neighboursThis))
        return neighbourtrianglesIndices
    
    def findStartTriangle(self,index):
        '''returns the index of one triangle touching the node index'''
        for i in range(len(self.faces)):
            if index in self.faces[i]:
                return i

    def getSuroundingTriangles(self):
        '''returns a list of triangles surrounding the node'''
        for i in range(len(self.vertices)):
            start = self.findStartTriangle(i)#index innerhalb von self.faces!
            






def correctList(old):
    '''ensures that each element appears only once in the list'''
    new=[]
    for i in old:
        if i in new:
            continue
        else:
            new.append(i)
    return new

mesh = CylindricMesh(2,1,10)

#TODO test function for normals (nach außen und alle gleich!)

def test_EqualDirectionsNormal(mesh): #WIP
    for i in range(len(mesh.faces)):
        print("Normle Dreieck Nummer ",i, "ist" , calculateNormal(mesh,mesh.faces[i]))

def test_IfLonelyVertice(mesh):
    for i in range(len(mesh.vertices)):
        if(any(i in sublist for sublist in mesh.faces)):
             continue
        else:print("LONELY POINT: ", i)   
    print("finished test")


def calculateNormal(mesh,face):
    if len(face) == 3:
        point0 = mesh.vertices[face[0]]
        point1 = mesh.vertices[face[1]]
        point2 = mesh.vertices[face[2]]
        v1 = point1 - point0
        v2 = point2 - point0
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
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')

#X=[]
#Y=[]
#Z=[]
#for i in range(len(mesh.vertices)):
#    X.append(mesh.vertices[i][0])
#    Y.append(mesh.vertices[i][1])
#    Z.append(mesh.vertices[i][2])
#ax.scatter3D(X,Y,Z)
#plt.show()
