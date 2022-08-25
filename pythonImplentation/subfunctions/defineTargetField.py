#kugel in zylinder, gleichmäßig im Volumen verteilte Punkte, mit gewünschtem Feld (absolute Werte?)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TargetField():
    def __init__(self,center,radius,direction):#direction: 0==x,1==y,2==z
        self.center = center
        self.radius = radius
        self.vertices = self.getTargetPoints()
        self.fieldValues = self.getMagneticFieldInPoints(direction)

    def getTargetPoints(self):
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
        return targetVertices

    def getMagneticFieldInPoints(self,direction):#0==x,1==y,2==z
        #normiert die Werte -> mapping auf 0 bis 1 was als gewünschtes Feld definiert werden kann 
        magneticFieldValues=[]
        distance=np.max(self.vertices[direction])-np.min(self.vertices[direction])
        for i in range(len(self.vertices[direction])):
            magneticFieldValues.append((self.vertices[direction][i]-np.min(self.vertices[direction]))/distance)
        return magneticFieldValues

def distanceBetweenPoints(point1,point2):
    result = 0
    for i in range(len(point1)):
        result += (point1[i]-point2[i])**2
    return np.sqrt(result)


#sphere=TargetField([0,0,0],5,1)
#points = sphere.vertices
#print(np.shape(points))
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')

#ax.scatter3D(points[0],points[1],points[2])
#plt.show()