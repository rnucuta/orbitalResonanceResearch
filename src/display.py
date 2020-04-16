import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from math import *
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from scipy.spatial import ConvexHull
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
import numpy as np
import scipy as sp
from scipy import spatial as sp_spatial
# from temp import te
from stl_editor import angles, shadows

def main():
	# angle = angles(400)
	shadow = shadows(400)
	#print(shadow)
	final_temps = 0#te()
	hexes = []
	time = 0
	for i in range(206):
		#T = final_temps[time][i]
		#mini = min(final_temps[time])
		#maxi = max(final_temps[time])
		#value = RGB(T, mini, maxi)
		hexes.append('#FF0000')
		#hexes.append('#FF0000')

	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlim3d(-100, 100)
	ax.set_ylim3d(-100, 100)
	ax.set_zlim3d(-100, 100)
	file_name = '207tri_sphere.stl'
	#sphere_mesh1 = mesh.Mesh.from_file(file_name)
	plotter = pv.Plotter()
	sphere_mesh = pv.read(file_name)

	# fc = []
	# for i in range(206):
	# 	if i % 2 == 0:
	# 		fc.append('white')
	# 	else:
	# 		fc.append('orange')

	# fc = hexes 

	# color = []

	# for i in fc:
	# 	color.append(i.upper())

	
	# print(color)









	#plotter.add_mesh(sphere_mesh, scalars = color)
	#plotter.show()






	x = []
	y = []
	z = []


	vertices = sphere_mesh.points

	faces = []
	values = sphere_mesh.faces
	for i in range(206):
		if shadow[i][0] == 1:
			face = []
			index = 1
			for j in range(3):
				face.append(values[4*(i) + index])
				index += 1
			faces.append(face)
	


	for i in faces:
		index = faces.index(i)
		for j in range(3):
			x.append(vertices[i[j]][0])
			y.append(vertices[i[j]][1])
			z.append(vertices[i[j]][2])
		verts = [list(zip(x, y, z))]
		ax.add_collection3d(Poly3DCollection(verts))
		x = []
		y = []
		z = []

	plt.show()










	# normal = sphere_mesh.face_normals
	# normal1 = sphere_mesh1.normals

	# #print(normal)


	# for i in range(len(normal1)):
	# 	mag = np.linalg.norm(normal1[i])
	# 	normal1[i][0] = normal1[i][0]/mag
	# 	normal1[i][1] = normal1[i][1]/mag
	# 	normal1[i][2] = normal1[i][2]/mag
	
	#print(normal1)


	# test = False
	# for i in range(sphere_mesh.number_of_faces):
	# 	for j in range(3):
	# 		if not sphere_mesh.face_normals[i][j] == sphere_mesh1.normals[i][j]:
	# 			test = True

	# if test:
	# 	print("FUCK")
	# else:
	# 	print("YAY")
	







def RGB(T, mini, maxi):
	Rt = R(T, mini, maxi)
	#Gt = G(T)

	# if len(Rt) < 2:
	# 	Rt = '0' + str(Rt) 

	if len(Rt) < 2:
		Rt = '0' + str(Rt) 
	return ('#' + str(Rt) + '00' + '00')



def R(T, mini, maxi):
	diff = maxi - mini
	G = (255/diff)*(T-mini)

	if G < 0:
		G = 0

	if G > 255:
		G = 255

	return hex(floor(G))[2:]

def G(T):
	return hex(255)[2:]


main()







