import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from math import *

file_name = '207tri_sphere.stl'
sphere_mesh = mesh.Mesh.from_file(file_name)
normal_vectors = sphere_mesh.normals
#runs angle for each time_steps and rerturns 2d array
def angles(time_steps):
	#sphere_mesh = mesh.Mesh.from_file(file_name)
	volume, cog, inertia = sphere_mesh.get_mass_properties()
	#normal_vectors = sphere_mesh.normals
	facets = len(normal_vectors)
	angles = [[0 for j in range(facets)] for i in range(time_steps)]
	for i in range(time_steps):
		angles[i] = (angle([1, 0, 0], facets))

		rotate(time_steps, cog)

	#convert angles into facet by time
	#angles1 = [[0 for j in range(time_steps)] for i in range(facets)]
	angles1 = []
	for i in range(facets):
		te = []
		for j in range(time_steps): 
			te.append(angles[j][i])
	
		angles1.append(te)

	return angles1

def facetNumber():
	#sphere_mesh = mesh.Mesh.from_file(file_name)
	normal_vectors = sphere_mesh.normals
	return len(normal_vectors)

#calculate angle for each facet
def angle(ray_vector, facets):
	
	angles = [0 for i in range(facets)]
	#ray_vector = [-1, 0, 0]

	j = 0
	for i in normal_vectors:
		# back_side = False
		# if i[0] < 0:
		# 	back_side = True

		# left_side = False
		# if i[1] < 0:
		# 	left_side = True

		cross_p = np.dot(ray_vector, i)
		normal_mag = np.linalg.norm(i)
		equ = np.linalg.norm(cross_p/normal_mag)

		#if z is negative for cross product
		#right negative
		#left postive

		#angle = asin(equ)
		if equ > 1:
			equ = 1

		angles[j] = acos(equ)
		#angles[j] = 0
		j += 1

	return angles


def rotate(time_steps, cog):

	radians = (2*pi)/time_steps
	r_matrix = [[cos(radians), -sin(radians), 0], [sin(radians), cos(radians), 0], [0, 0, 1]]

	for i in range(len(normal_vectors)):
		new_vector = []
		vector = normal_vectors[i]
		for j in range(3):
			number = 0
			for k in range(3):
				number += r_matrix[j][k]*vector[k]
			new_vector.append(number)

		normal_vectors[i] = new_vector

	
	#degrees = (radians*180)/pi
	#mesh.rotate([0, 0, 1], radians, point=cog)

def shadow():
	shadows = []
	j = 0
	for i in normal_vectors:
		back_side = False
		if i[0] > 0:
			back_side = True


		if back_side:
			shadows.append(0)
		else:
			shadows.append(1)

		j += 1

	return shadows

def shadows(time_steps):
	#sphere_mesh = mesh.Mesh.from_file(file_name)
	volume, cog, inertia = sphere_mesh.get_mass_properties()
	#normal_vectors = sphere_mesh.normals
	facets = len(normal_vectors)
	shadows = [[0 for j in range(facets)] for i in range(time_steps)]
	for i in range(time_steps):
		shadows[i] = (shadow())
		
		rotate(time_steps, cog)

	#convert angles into facet by time
	#angles1 = [[0 for j in range(time_steps)] for i in range(facets)]
	shadows1 = []
	for i in range(facets):
		te = []
		for j in range(time_steps):
			te.append(shadows[j][i])
			#print(shadows[j][i])
			
		shadows1.append(te)

	#print(angles1)
	return shadows1

def display():
	# Create a new plot
	figure = pyplot.figure()
	axes = mplot3d.Axes3D(figure)

	# Render the cube
	axes.add_collection3d(mplot3d.art3d.Poly3DCollection(sphere_mesh.vectors))

	#Auto scale to the mesh size
	scale = sphere_mesh.points.flatten('C')
	axes.auto_scale_xyz(scale, scale, scale)

	# Show the plot to the screen
	pyplot.show()





