### Input

### MESH
# generate mesh: define Cylindric_mesh, coil_mesh.vertices (Eckpunkte), coil_mesh.faces(Oberflächen)
from python.subfunctions.read_mesh import Cylindric_mesh
Mesh = Cylindric_mesh(5.0,3.0,100)

# not relevant for a generated cylindric mesh: split_disconnected_mesh(Trennt Objekte falls mehrere unverbundene Netze im stl), refine_mesh(Macht aus einem Dreieck 3)


### STREAM FUNCTION
# parameterize the mesh: normalen, Planarization, offene Boundaries markieren (Liste welche vertices), auf 2D (evtl z-Axen ausrichtung dafür)

# define target field

# calculate one ring by mesh: Liste mit allen direkten Nachbarknoten für jeden Knoten 

# basisfunktionen: Mikrospulen um jeden Knoten -> werden in sensitifity matrix mit dem Zielfeld in Verbindung gebracht

### Calculation

# stream function optimization

# 2D surface projection

# potential discretization

# topological contour sorting

# opening and interconnection wires


### Output

# plots

# ouput for 3D

class Coil():
    def __init__(self,tikonov_factor):
        self.tikonov_factor = tikonov_factor
