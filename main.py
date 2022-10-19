import numpy as np

### Input #################
meshFile = "C:\\Users\Simone\git\Py-CoilGen\cylinder_radius500mm_length1500mm.stl" #insert Filename of stl mesh or False here
targetMeshFile = "C:\\Users\Simone\git\Py-CoilGen\sphere_radius150mm.stl" #insert Filename of stl mesh or False here
gaussOrder = 2
tikonovFac = 100
specificConductivityMaterial = 1.8000*10**-8
conducterThickness = 0.005 
materialFactor = specificConductivityMaterial/conducterThickness

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
sensitivityMatrix = getSensitivityMatrix(Mesh,TargetSphere,gaussOrder)

#resistance matrix
from subfunctions.resistanceMatrix import getResistanceMatrix
resistanceMatrix = getResistanceMatrix(Mesh,materialFactor)

### Calculation ############

# stream function optimization
from subfunctions.streamFunctionOptimization import streamFunctionOptimization
streamFunction = streamFunctionOptimization(Mesh,TargetSphere,sensitivityMatrix,resistanceMatrix,tikonovFac)
print("SF",streamFunction)

# 2D surface projection

# potential discretization

# topological contour sorting

# opening and interconnection wires

### Output

# plots

# ouput for 3D


