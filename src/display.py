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

	#shadow
	with open('./shadow_data.data', 'rb') as f:
		shadow = pickle.load(f)

	#thermal map
	with open('./temp_obj.obj', 'rb') as f:
		Temperature = pickle.load(f)
	final_temps = Temperature.final_temps

	#color
	hexes = []
	time = 0
	mini = min(final_temps[time])
	maxi = max(final_temps[time])
	for i in range(206):
		T = final_temps[time][i]
		value = RGB(T, mini, maxi)
		hexes.append(value)

	


	#plotting
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlim3d(-100, 100)
	ax.set_ylim3d(-100, 100)
	ax.set_zlim3d(-100, 100)
	file_name = '207tri_sphere.stl'
	plotter = pv.Plotter()
	sphere_mesh = pv.read(file_name)

	
	x = []
	y = []
	z = []


	vertices = sphere_mesh.points

	faces = []
	values = sphere_mesh.faces
	for i in range(206):
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
		ax.add_collection3d(Poly3DCollection(verts, hexes))
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







