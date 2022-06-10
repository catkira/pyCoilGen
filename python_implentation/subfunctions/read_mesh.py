# we need mesh, vertices and faces from the mesh

#option 1: given mesh 
#option 2: create cylindric mesh 
import numpy as np
import matplotlib.pyplot as plt
import pymesh
import meshzoo

class Cylindric_mesh():
    def __init__(self,coil_length,coil_radius,coil_n):
        self.vertices, self.faces = meshzoo.tube(length=coil_length, radius=coil_radius, n=int(coil_n))#points, cells(index of the points that close the cell)

mesh = Cylindric_mesh(2,0.5,10)


#Fall das faces nicht aus 3 Komponenten besteht im Kopf behalten, evtl bei direkter Mesh Einspeisung handeln. (create_unique_noded_mesh)

#print(mesh.vertices,mesh.faces)
#po bottom center
#p1 top center
#ro_out bottom outer radius 
#radius = 5
#funciton just in c++?
#quadMesh = pymesh.generate_tube(np.array([0,0,7]), np.array([0,0,1]), radius, radius, radius, radius, num_segments=16, with_quad=True)
#print(pymesh.quad_to_tri(quadMesh, keep_symmetry=False))


#cylinder(pos=(-2,0,0), axis=(3,1,0), radius=1)
# #print(cylinder)
# r= 2
# laenge = 5
# theta = np.linspace(0,2*np.pi,100)
# x = r*np.sin(theta)
# y = r*np.cos(theta)
# #xx,yy = np.meshgrid(x,y)
# z = np.linspace(-laenge/2,laenge/2, 10000)
#print(open3d.geometry.create_mesh_cylinder(radius=1.0, height=2.0, resolution=20, split=4))

# points = np.c_[xx.reshape(-1), yy.reshape(-1), z.reshape(-1)]
# points[0:5, :]
# cloud = pv.PolyData(points)
# cloud.plot(point_size=15)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# r = np.linspace(1, 1, 50)
# p = np.linspace(0, 2*np.pi, 50)
# R, P = np.meshgrid(r, p)
# Z = ((R**2 - 1)**2)
X=[]
Y=[]
Z=[]
for i in range(len(mesh.vertices)):
    X.append(mesh.vertices[i][0])
    Y.append(mesh.vertices[i][1])
    Z.append(mesh.vertices[i][2])
ax.scatter3D(X,Y,Z)
plt.show()
# # Tweak the limits and add latex math labels.
# ax.set_zlim(0, 1)
# ax.set_xlabel(r'$\phi_\mathrm{real}$')
# ax.set_ylabel(r'$\phi_\mathrm{im}$')
# ax.set_zlabel(r'$V(\phi)$')
