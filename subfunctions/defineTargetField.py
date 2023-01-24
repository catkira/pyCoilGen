#kugel in zylinder, gleichmäßig im Volumen verteilte Punkte, mit gewünschtem Feld 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from readMesh import getMeshFromSTL


class TargetField():
    def __init__(self,center,radius,direction):#direction: 0==x,1==y,2==z
        self.center = center
        self.radius = radius
        self.vertices = self.getTargetPoints()
        self.fieldValues = self.getMagneticFieldValues(direction)

    def getTargetPoints(self):
        '''generate Target Points within a circle with the given specifications'''
        newX = np.linspace(self.center[0]-self.radius,self.center[0]+self.radius,25)
        newY = np.linspace(self.center[1]-self.radius,self.center[1]+self.radius,25)
        newZ = np.linspace(self.center[2]-self.radius,self.center[2]+self.radius,25)
        newX,newY,newZ = np.meshgrid(newX, newY, newZ, indexing='ij')
        targetVertices = []
        for i in range(len(newX)):
            for j in range(len(newX)):
                for k in range(len(newX[i][j])):
                    if distanceBetweenPoints(self.center,[newX[i][j][k],newY[i][j][k],newZ[i][j][k]]) <= self.radius:
                        targetVertices.append([newX[i][j][k],newY[i][j][k],newZ[i][j][k]])
                    else: continue 
        return np.array(targetVertices)#array is important to be able to do [:,0]

    def getMagneticFieldValues(self,direction):
        '''returns magnetic field values analogus to matlab skript'''
        targetStrength = 1
        targetField = np.zeros((3,len(self.vertices)))
        targetField[2] = self.vertices[:,direction]
        targetField = targetField*targetStrength
        return targetField

class TargetFieldGiven(TargetField):
    def __init__(self,filename,direction):
        self.vertices,self.faces = getMeshFromSTL(filename)
        self.fieldValues = self.getMagneticFieldValues(direction)

def distanceBetweenPoints(point1,point2):
    '''returns the distance between two given points'''
    result = 0
    for i in range(len(point1)):
        result += (point1[i]-point2[i])**2
    return np.sqrt(result)

## Testing ###
#sphere=TargetField([0,0,0],5,1)
#points = sphere.vertices
#print(np.shape(points))
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')

#ax.scatter3D(points[0],points[1],points[2])
#plt.show()