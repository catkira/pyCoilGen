import numpy as np
from decimal import *
import sys
sys.path.append('source/')


### Testing ###############
from Tester import Tester
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

from readMesh import CylindricMesh,CylindricMeshGiven
if meshFile:
    Mesh = CylindricMeshGiven(meshFile)
else: Mesh = CylindricMesh(5.0,3.0,10) 

from defineTargetField import TargetField,TargetFieldGiven
if targetMeshFile:
    TargetSphere = TargetFieldGiven(targetMeshFile,1)
else: TargetSphere = TargetField([0,0,0],4,1)

from sensitivityMatrix import getSensitivityMatrix
sensitivityMatrix = getSensitivityMatrix(Test,Mesh,TargetSphere,gaussOrder)

from resistanceMatrix import getResistanceMatrix
resistanceMatrix = getResistanceMatrix(Test,Mesh,materialFactor)

### Calculation ############

from streamFunctionOptimization import streamFunctionOptimization
bFieldGeneratedByOptSF,streamFunction = streamFunctionOptimization(Test,Mesh,TargetSphere,sensitivityMatrix,resistanceMatrix,tikonovFac)

from calcPotentialLevels import calcPotentialLevels
contourStep, potentialLevelList = calcPotentialLevels(streamFunction, numLevels, levelOffset)

from source.calcContoursByTriangularPotentialCuts import calcContoursByTriangluarPotentialCuts
contour = calcContoursByTriangluarPotentialCuts(Mesh,potentialLevelList,streamFunction)

# topological contour sorting

# opening and interconnection wires

### Output

# plots

# ouput for 3D
