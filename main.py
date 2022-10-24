import numpy as np
from decimal import *
import sys
sys.path.append('subfunctions/')


##### Testing #############
from subfunctions.Tester import Tester
Test = Tester()

### Input #################
meshFile = "cylinder_radius500mm_length1500mm.stl" #insert Filename of stl mesh or False here
targetMeshFile = "sphere_radius150mm.stl" #insert Filename of stl mesh or False here
gaussOrder = 2
tikonovFac = 100
specificConductivityMaterial = 1.8000*10**-8
conducterThickness = 0.005 
materialFactor = specificConductivityMaterial/conducterThickness
numLevels = 20
levelOffset = 0.2500

### MESH ##################

# generate mesh
from subfunctions.readMesh import CylindricMesh,CylindricMeshGiven
if meshFile:
    Mesh = CylindricMeshGiven(meshFile)
else: Mesh = CylindricMesh(5.0,3.0,10) #length,radius,n
print("vertices",np.shape(Mesh.vertices),"faces",np.shape(Mesh.faces))

# define target field
from subfunctions.defineTargetField import TargetField,TargetFieldGiven
if targetMeshFile:
    TargetSphere = TargetFieldGiven(targetMeshFile,1)
else: TargetSphere = TargetField([0,0,0],4,1) #center,radius,direction
print("vertices",np.shape(TargetSphere.vertices),"faces",np.shape(TargetSphere.faces))

#sensitivity matrix
from subfunctions.sensitivityMatrix import getSensitivityMatrix
sensitivityMatrix = getSensitivityMatrix(Test,Mesh,TargetSphere,gaussOrder)


def getListFormatedForComparing(list):
    result = ""
    for i in range(len(list)):            
        my_list_str = [str(x) for x in list[i]]
        max_decimal = max([ len(x) - x.find('.') - 1 for x in my_list_str])
        fmt_str = f"%0.{max_decimal+9}f"
        my_list_str = [fmt_str % x for x in list[i]]
        if result == "":
            result = "[" + ", ".join(my_list_str) + "]"
        else: result = result + "," + "[" + ", ".join(my_list_str) + "]"
        
    return result
#resistance matrix
from subfunctions.resistanceMatrix import getResistanceMatrix
resistanceMatrix = getResistanceMatrix(Test,Mesh,materialFactor)

### Calculation ############

# stream function optimization
from subfunctions.streamFunctionOptimization import streamFunctionOptimization
bFieldGeneratedByOptSF,streamFunction = streamFunctionOptimization(Test,Mesh,TargetSphere,sensitivityMatrix,resistanceMatrix,tikonovFac)

# potential discretization
from subfunctions.calcPotentialLevels import calcPotentialLevels
contourStep, potentialLevelList = calcPotentialLevels(streamFunction, numLevels, levelOffset)

#print("etv",Test.matElementsShouldGetValue)

from subfunctions.calcContoursByTriangularPotentialCuts import calcContoursByTriangluarPotentialCuts
contour = calcContoursByTriangluarPotentialCuts(Mesh,potentialLevelList,streamFunction)

# topological contour sorting

# opening and interconnection wires

### Output

# plots

# ouput for 3D
