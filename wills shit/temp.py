import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sympy import solve
from sympy import Symbol
from math import *
from stl_editor import angles, facetNumber, shadow

#constants

#pi
P = 21768.516 #period of rotation(spin)(seconds)
gamma = 110 #sqrt(k*rho*C) thermal inertia
k = 4.5 #thermal conductivity #UNKNOWN
rho = 1800#density #UNKNOWN
C = (gamma**2)/(k*rho)#specific heat capacity #UNKNOWN
E = 0.7 #emissivity
S = 5.67 * (10**-8)#Stefan–Boltzmann constant
Wsun = 1367 #Power from sun (Wsun/(rh)^2)(W/m^2)
Ab = 0.24 #Bond Albedo
z = sqrt((4*pi*P*k)/(rho*C)) #normalized depth
t = P #normalized time

#Things to be determined
r = 2.3633 #distance from Sun(AU)
depth_steps = 5 #number of depth steps
time_steps = 10 #number of time steps
facets = facetNumber() #number of facets
cos = angles(time_steps)#si(t), cos(feta) #2d array #UNKNOWN
shadow = shadow(cos, facets, time_steps)#1-not shadowed 0-shadowed #2d array #UNKNOWN
dz = 2/depth_steps #change in z #0-depth_steps-1
dt = 1/time_steps #change in t #0-time_steps-1
Tacc = 1#min change in T #UNKNOWN



def main():
	#initialize
	temp = [[0 for k in range(depth_steps)] for i in range(facets)] #facet by depth
	#temp_temporary = [0 for i in range(depth_steps)]
	#for calculating accuracy
	surface_temp = [0 for j in range(2*time_steps)] #temp of top depth for each time for one facet
	#time = 0

	#for facets
	for facet_num in range(facets):
		#initialize temperatures
		j = 0 #time
		temp_temporary = setTemp(facet_num)
		temp[facet_num] = temp_temporary[:]
		
		#until accurate repeat facet
		while j < time_steps or not isAccurate(j, surface_temp):
			#test
			if j > time_steps:
				break
			#test

			#storing previous temps
			if j < time_steps:
				surface_temp[j] = temp[facet_num][0]
			else:
				integer = floor(j/(2*time_steps))
				surface_temp[j-integer*2*time_steps] = temp[facet_num][0]

			#for depth steps
			for i in range(depth_steps):
				#top
				if i == 0:
					temp_temporary[i] = solveExternalBC(facet_num, j, temp)
					continue

				#bottom
				if i == depth_steps-1:
					#This assigns a reference but technically that doesnt matter
					temp_temporary[i] = temp_temporary[i-1]
					continue

				#everything else
				temp_temporary[i] = solveDepthTemp(facet_num, i, temp)

			#set temps
			temp[facet_num] = temp_temporary[:]
			#change time
			j += 1

		print(str(facet_num) + ": hey")
	print(temp)
	#fix deep copy in stl_editor in angles()
	#check for other array copy mistakes
	#fix weird temperature
	#do shadows next
					
#calculates Tmean for a facet
def Tmean(facet_num): 
	constant = (((1-Ab)/(E*S))**1/4)
	sums = 0
	for j in range(time_steps):
		shade = shadow[facet_num][j]
		angle = cos[facet_num][j]
		Fsun = Wsun/(r*r)
		sums += shade*angle*Fsun

	return (constant*sums)/t

#assigns an initial temperature to all depth steps for a facet
def setTemp(facet_num):
	temperature = [0 for j in range(depth_steps)]
	mean = Tmean(facet_num)
	for i in range(depth_steps):
		Ti = mean*exp(-2*pi*i*dz)
		temperature[i] = Ti

	return temperature

#solves external BC, returns temp
def solveExternalBC(facet_num, j, temp):
	integer = floor(j/(time_steps))
	j = j-integer*time_steps
	shade = shadow[facet_num][j]
	angle = cos[facet_num][j]
	Fsun = Wsun/(r*r)
	T1 = temp[facet_num][1];
	# print(shade)
	# print(T1)
	T = Symbol('T')
	solution = solve((1-Ab)*shade*angle*Fsun + (gamma/(sqrt(4*pi*P)))*((T1-T)/dz) - E*S*(T**4), T)
	return solution[0]
#solve temperature for depth steps
def solveDepthTemp(facet_num, depth, temp):
	Tabove = temp[facet_num][depth - 1]
	#print(Tabove)
	Tdepth = temp[facet_num][depth]
	#print(Tdepth)
	Tbelow = temp[facet_num][depth + 1]
	#print(Tbelow)

	return Tdepth + (1/(4*pi))*(dt/(dz**2))*(Tbelow - 2*Tdepth + Tabove)

#boolean - returns true if accurate enough
#Consider using the energy method
def isAccurate(j, surface_temp):
	integer = floor(j/(time_steps))
	j = j-integer*time_steps
	diff = abs(surface_temp[j+time_steps] - surface_temp[j])
	if diff <= Tacc:
		return True
	
	return False

main()
