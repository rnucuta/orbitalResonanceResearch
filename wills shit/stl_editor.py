import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from math import *

file_name = '207tri_sphere.stl'
def angles(time_steps):
	sphere_mesh = mesh.Mesh.from_file(file_name)
	volume, cog, inertia = sphere_mesh.get_mass_properties()
	normal_vectors = sphere_mesh.normals
	facets = len(normal_vectors)
	angles = [[0 for j in range(facets)] for i in range(time_steps)]
	for i in range(time_steps):
		angles[i] = (angle(sphere_mesh, [-1, 0, 0], facets, normal_vectors))

		rotate(sphere_mesh, time_steps, cog)

	#convert angles into facet by time
	#angles1 = [[0 for j in range(time_steps)] for i in range(facets)]
	angles1 = []
	for i in range(facets):
		te = []
		for j in range(time_steps):
			te.append(angles[j][i])
		angles1.append(te)

	#print(angles1)
	return angles1

def facetNumber():
	sphere_mesh = mesh.Mesh.from_file(file_name)
	normal_vectors = sphere_mesh.normals
	return len(normal_vectors)

def angle(mesh, ray_vector, facets, normal_vectors):
	
	angles = [0 for i in range(facets)]
	#ray_vector = [-1, 0, 0]

	j = 0
	for i in normal_vectors:
		back_side = False
		if i[0] < 0:
			back_side = True

		left_side = False
		if i[1] < 0:
			left_side = True

		cross_p = np.cross(ray_vector, i)
		normal_mag = np.linalg.norm(i)
		equ = np.linalg.norm(cross_p/normal_mag)

		#if z is negative for cross product
		#right negative
		#left postive
		if cross_p[2] < 0:
			equ = -equ

		angle = asin(equ)

		#radians to degrees
		angle = (angle*180)/pi

		# convert to 0-360 scale
		if back_side:
			angle += 180
		elif left_side:
			angle += 270
		else:
			angle = -angle
			

		angles[j] = angle
		j += 1

	return angles


def rotate(mesh, time_steps, cog):
	

	radians = (2*pi)/time_steps
	degrees = (radians*180)/pi
	mesh.rotate([0, 0, 1], degrees, point=cog)


def display(mesh):
	# Create a new plot
	figure = pyplot.figure()
	axes = mplot3d.Axes3D(figure)

	# Render the cube
	axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))

	#Auto scale to the mesh size
	scale = mesh.points.flatten('C')
	axes.auto_scale_xyz(scale, scale, scale)

	# Show the plot to the screen
	pyplot.show()

def shadow(cos, facets, time_steps):
	shadows = []
	for i in range(facets):
		shadow = []
		for j in range(time_steps):
			angle = cos[i][j]
			if angle > 270 or angle < 90:
				shadow.append(1)
			else:
				shadow.append(0)

		shadows.append(shadow)

	return shadows