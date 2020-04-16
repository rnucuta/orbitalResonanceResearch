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
# from temp import te
#from stl_editor import angles, shadows

def main():
	#initialize
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlim3d(-4, 4)
	ax.set_ylim3d(-4, 4)
	ax.set_zlim3d(-4, 4)
	file_name = 'Steins350.stl'
	plotter = pv.Plotter()
	sphere_mesh = pv.read(file_name)

	#shadow
	with open('./shadow_data.data', 'rb') as f:
		shadow = pickle.load(f)

	#thermal map
	with open('./temp_obj.obj', 'rb') as f:
		Temperature = pickle.load(f)
	final_temps = Temperature.final_temps
	file_length = len(final_temps[0])

	#angle
	angle = Temperature.thermalmap_obj.phi(400)
	angles = [[0 for k in range(file_length)] for i in range(400)]
	#facet
	for i in range(len(angle)):
		#time
		for j in range(len(angle[0])):
			angles[j][i] = angle[i][j]

	#color
	hexes = []
	time = 0
	# mini = min(final_temps[time])
	# maxi = max(final_temps[time])
	mini = min(angles[time])
	maxi = max(angles[time])
	for i in range(file_length):
		#T = final_temps[time][i]
		T = abs(angles[time][i])
		value = RGB(T, mini, maxi)
		hexes.append(value)

	


	#plotting
	x = []
	y = []
	z = []


	vertices = sphere_mesh.points

	faces = []
	values = sphere_mesh.faces
	for i in range(file_length):
		if i in shadow[0]:
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







