import numpy
from stl import mesh

asteroid_stl = mesh.Mesh.from_file('toutatis.stl')

normal_vectors=asteroid_stl.normals

numpy.save("toutatis_normals", normal_vectors)

