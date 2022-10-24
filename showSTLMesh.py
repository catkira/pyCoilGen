import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def getMesh(filename):
    your_mesh = mesh.Mesh.from_file(filename)
    normals = your_mesh.normals
    vertices = [your_mesh.v0, your_mesh.v1, your_mesh.v2]
    return normals, vertices

class CylindricMeshGiven():
    def __init__(self):
        self.normals, self.vertices = getMesh('cylinder_radius500mm_length1500mm.stl')

        
givenMesh = CylindricMeshGiven()
print("mesh",givenMesh.normals)


# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Using an existing stl file:


your_mesh = mesh.Mesh.from_file('cylinder_radius500mm_length1500mm.stl')

print(your_mesh.normals)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))


# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()