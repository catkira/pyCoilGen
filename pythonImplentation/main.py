### Input
import numpy as np
### MESH
# generate mesh: define Cylindric_mesh, coil_mesh.vertices (Eckpunkte), coil_mesh.faces(Oberflächen)
from subfunctions.readMesh import CylindricMesh
Mesh = CylindricMesh(5.0,3.0,10)
#print("vertices",Mesh.vertices)
#print("boundaries",Mesh.openBoundaries)
# with open("mesh", 'wb') as pickle_file:
#     pickle.dump(all, pickle_file)
# with open('mesh', 'rb') as pickle_file:
#     Mesh = pickle.load(pickle_file)
#Mesh = pickle.load('mesh.txt')
# not relevant for a generated cylindric mesh: split_disconnected_mesh(Trennt Objekte falls mehrere unverbundene Netze im stl), refine_mesh(Macht aus einem Dreieck 3)


### STREAM FUNCTION
# parameterize the mesh: normalen, Planarization, offene Boundaries markieren (Liste welche vertices), auf 2D (evtl z-Axen ausrichtung dafür)

# define target field
from subfunctions.defineTargetField import TargetField
TargetSphere = TargetField([0,0,0],4,1)#center,radius,direction

# calculate one ring by mesh: Liste mit allen direkten Nachbarknoten für jeden Knoten (in readMesh)

#-------

from subfunctions.sensitivityMatrix import getSensitivityMatrix

gaussOrder = 2
sensitivityMatrix = getSensitivityMatrix(Mesh,TargetSphere,gaussOrder)

from subfunctions.resistanceMatrix import getResistanceMatrix

resistanceMatirx = getResistanceMatrix(Mesh)
# basisfunktionen: vorberechnungen für sensitivity matrix -> werden in sensitivity matrix mit dem Zielfeld in Verbindung gebracht (in readMesh)
tikonovFac = 10000
from subfunctions.streamFunctionOptimization import streamFunctionOptimization
streamFunction = streamFunctionOptimization(Mesh,TargetSphere,sensitivityMatrix,resistanceMatirx,tikonovFac)

### Calculation

# stream function optimization

# 2D surface projection

# potential discretization

# topological contour sorting

# opening and interconnection wires


### Output

# plots

# ouput for 3D


