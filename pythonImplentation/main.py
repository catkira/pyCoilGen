import numpy as np

### Input #################
meshFile = 'cylinder_radius500mm_length1500mm.stl' #insert Filename of stl mesh or False here
targetMeshFile = 'sphere_radius150mm.stl' #insert Filename of stl mesh or False here
gaussOrder = 2
tikonovFac = 100


### MESH ##################

# generate mesh
from subfunctions.readMesh import CylindricMesh,CylindricMeshGiven
if meshFile:
    Mesh = CylindricMeshGiven(meshFile)
else: Mesh = CylindricMesh(5.0,3.0,10) #length,radius,n

# define target field
from subfunctions.defineTargetField import TargetField,TargetFieldGiven
if targetMeshFile:
    TargetSphere = TargetFieldGiven(targetMeshFile,1)
else: TargetSphere = TargetField([0,0,0],4,1) #center,radius,direction

#sensitivity matrix
from subfunctions.sensitivityMatrix import getSensitivityMatrix
sensitivityMatrix = getSensitivityMatrix(Mesh,TargetSphere,gaussOrder)

#resistance matrix
from subfunctions.resistanceMatrix import getResistanceMatrix
resistanceMatirx = getResistanceMatrix(Mesh)


### Calculation ############

# stream function optimization
from subfunctions.streamFunctionOptimization import streamFunctionOptimization
streamFunction = streamFunctionOptimization(Mesh,TargetSphere,sensitivityMatrix,resistanceMatirx,tikonovFac)

# 2D surface projection

# potential discretization

# topological contour sorting

# opening and interconnection wires


### Output

# plots

# ouput for 3D


