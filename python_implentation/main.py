### Input

from python.subfunctions.read_mesh import Cylindric_mesh
Mesh = Cylindric_mesh(5.0,3.0,100)
# generate mesh: define coil_mesh, coil_mesh.vertices (Eckpunkte), coil_mesh.faces(Oberflächen, Normalen(?))
# steps I'm not sure why and if we need them: split_disconnected_mesh, refine_mesh
#TODO: Ask Philipp if mesh meets requirements and try to find out if data have already the correct format

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
