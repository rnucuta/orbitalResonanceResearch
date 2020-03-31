import numpy
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d



sphere_stl = mesh.Mesh.from_file('207tri_sphere.stl')

normal_vectors = sphere_stl.normals

numpy.save("toutatis_normals", normal_vectors)

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Render the cube
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(sphere_stl.vectors))

# Auto scale to the mesh size
scale = sphere_stl.points.flatten('C')
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()