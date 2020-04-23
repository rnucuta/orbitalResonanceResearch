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
import pickle
import math
from yarkovsky import Yarkovsky
# from temp import te
#from stl_editor import angles, shadows

def main():
	# position = [-0.5304365993252850*5, 2.593585584222165*5, 0.3341370462881209*5]
	# position1 = [5.304365993252850*0.1, -2.593585584222165, -3.341370462881209*0.1]
	#initialize
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlim3d(-4, 4)
	ax.set_ylim3d(-4, 4)
	ax.set_zlim3d(-4, 4)
	file_name = 'Steins1500.stl'
	plotter = pv.Plotter()
	sphere_mesh1 = mesh.Mesh.from_file(file_name)

	#orient
	v = [-0.0059690746,-0.0163998975,-0.9998476952]
	itheta = math.acos(-0.9998476952)
	axis = np.cross(v,[0,0,1])
	sphere_mesh1.rotate(axis,itheta)
	
	#sphere_mesh1.save('Steins1500New.stl')
	sphere_mesh = pv.read('Steins1500New.stl')

	#shadow
	with open('./1500shadow_data_june.data', 'rb') as f:
		shadow = pickle.load(f)

	#thermal map
	with open('./1500temp_obj_june.obj', 'rb') as f:
		Temperature = pickle.load(f)
	final_temps = Temperature.final_temps
	file_length = len(final_temps[0])
	print(file_length)
	Yark = Yarkovsky(Temperature)
	force = Yark.yarkovskyforce()
	torque = Yark.yorptorque()
	print("force: " + str(force) + " torque: " + str(torque))
	

	#angle
	# angle = Temperature.thermalmap_obj.phi(400)
	# angles = [[0 for k in range(file_length)] for i in range(400)]

	
	# #facet
	# for i in range(len(angle)):
	# 	#time
	# 	for j in range(len(angle[0])):
	# 		angles[j][i] = angle[i][j]

	#color
	hexes = []
	time = 0
	mini = min(final_temps[time])
	maxi = max(final_temps[time])
	# mini = min(angles[time])
	# maxi = max(angles[time])
	for i in range(file_length):
		T = final_temps[time][i]
		# T = (angles[time][i])
		value = RGB(T, mini, maxi)
		hexes.append(value)

	print("done with color")


	#plotting
	x = []
	y = []
	z = []


	vertices = sphere_mesh.points

	faces = []
	values = sphere_mesh.faces
	for i in range(file_length):
		if (i-1) % 100 == 0:
			print(i)
		if i in shadow[0] or True:
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
		ax.add_collection3d(Poly3DCollection(verts, color = hexes[index]))
		x = []
		y = []
		z = []

	# origin = [0], [0] # origin point
	xf = force[0]
	yf = force[1]
	zf = force[2]

	#march
	# ax.quiver(0, 0, 0, -0.5304365993252850*5, 2.593585584222165*5, 0.3341370462881209*5, length=5, normalize=True)
	# ax.quiver(0, 0, 0, 0.5304365993252850*5, -2.593585584222165*5, -0.3341370462881209*5, length=5, normalize=True, color = 'red')
	# #Yarkovsky vector
	# ax.quiver(0, 0, 0, xf, yf, zf, length=5, normalize=True, color = 'green')


	# print("april")
	# #(1.520184545368283, 1.855273308408771, -3.439558151530418*0.01)
	# #away from sun
	# ax.quiver(0, 0, 0, 1.520184545368283, 1.855273308408771, -3.439558151530418*0.01, length=5, normalize=True)
	# #towards sun
	# ax.quiver(0, 0, 0, -1.520184545368283, -1.855273308408771, 3.439558151530418*0.01, length=5, normalize=True, color = 'red')
	# #Yarkovsky vector
	# ax.quiver(0, 0, 0, xf,  yf,  zf, length=5, normalize=True, color = 'green')
	

	print("june")
	# #(-2.290581730497342, -7.581072210604362*0.1,  2.546723138083118*0.1)
	# #away from sun
	ax.quiver(0, 0, 0, -2.290581730497342, -7.581072210604362*0.1,  2.546723138083118*0.1, length=5, normalize=True)
	# #towards sun
	ax.quiver(0, 0, 0, 2.290581730497342, 7.581072210604362*0.1,  -2.546723138083118*0.1, length=5, normalize=True, color = 'red')
	# #Yarkovsky vector
	ax.quiver(0, 0, 0, xf, yf, zf, length=5, normalize=True, color = 'green')
	
	plt.show()

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







