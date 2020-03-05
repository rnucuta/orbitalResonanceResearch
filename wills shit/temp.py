import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sympy import solve
from sympy import Symbol
from math import *
from stl_editor import angles, facetNumber, shadows

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
depth_steps = 500 #number of depth steps
time_steps = 300 #number of time steps
facets = facetNumber() #number of facets
feta = angles(time_steps)#si(t), feta(feta) #2d array #UNKNOWN
shadow = shadows(time_steps)#1-not shadowed 0-shadowed #2d array #UNKNOWN
# print(feta)
# print(shadow)
dz = 2/depth_steps #change in z #0-depth_steps-1
dt = 1/time_steps #change in t #0-time_steps-1
Tacc = 0.1#min change in T #UNKNOWN



def main():
	#initialize
	temp = [[0 for k in range(depth_steps)] for i in range(facets)] #facet by depth
	#temp_temporary = [0 for i in range(depth_steps)]
	#for calculating accuracy
	surface_temp = [0 for j in range(2*time_steps)] #temp of top depth for each time for one facet
	#time = 0

	#for facets
	for facet_num in range(facets-1, facets):
		#initialize temperatures
		j = 0 #time
		temp_temporary = setTemp(facet_num)
		temp[facet_num] = temp_temporary[:]
		
		#until accurate repeat facet
		while j < 10*time_steps or not isAccurate(j, surface_temp, facet_num):
			#test
			# if j > time_steps:
			# 	break
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
					temp_temporary[i] = solveExternalBC(facet_num, j, temp_temporary)
					continue

				#bottom
				if i == depth_steps-1:
					#This assigns a reference but technically that doesnt matter
					temp_temporary[i] = temp_temporary[i-1]
					continue

				#everything else
				temp_temporary[i] = solveDepthTemp(facet_num, i, temp_temporary)

			#set temps
			temp[facet_num] = temp_temporary[:]

			#change time
			j += 1
			#print(j)
		#print(str(facet_num) + ": hey")
	print(temp)

	hexes = []
	for i in range(facets):
		T = temp[i][0]
		value = RGB(T)
		hexes.append(value)
	#print(hexes)
	#fix deep copy in stl_editor in angles()
	#check for other array copy mistakes
	#fix weird temperature
	#do shadows next
					
#calculates Tmean for a facet
def Tmean(facet_num): 
	constant = (((1-Ab)/(E*S))**(1/4))
	sums = 0
	for j in range(time_steps):
		shade = shadow[facet_num][j]
		angle = cos(feta[facet_num][j])
		Fsun = Wsun/(r*r)
		sums += (shade*abs(angle)*Fsun)*dt
	#print(constant*((sums)**(1/4))/1)
	return (constant*((sums)**(1/4)))/1

#assigns an initial temperature to all depth steps for a facet
def setTemp(facet_num):
	temperature = [0 for j in range(depth_steps)]
	mean = Tmean(facet_num)
	for i in range(depth_steps):
		Ti = mean*(exp(-2*pi*i*dz))
		temperature[i] = Ti

	#print(temperature)
	return temperature

#solves external BC, returns temp
def solveExternalBC(facet_num, j, temp):
	integer = floor(j/(time_steps))
	j = j-integer*time_steps
	shade = shadow[facet_num][j]
	angle = feta[facet_num][j]
	Fsun = Wsun/(r*r)
	T1 = temp[1];
	# print(shade)
	# print(T1)
	#T = Symbol('T')
	#solution = solve((1-Ab)*shade*angle*Fsun + (gamma/(sqrt(4*pi*P)))*((T1-T)/dz) - E*S*(T**4), T)
	coeff = [-E*S, 0, 0, -(gamma/(sqrt(4*pi*P)*dz)), (1-Ab)*shade*angle*Fsun + (gamma/(sqrt(4*pi*P)*dz))*T1]
	solution  = np.roots(coeff)
	print(solution)
	for i in solution:
		if np.isreal(i) and i > 0:
			#print("real" + str(np.real(i)))
			return np.real(i)

	# print(solution)
	# return solution
#solve temperature for depth steps
def solveDepthTemp(facet_num, depth, temp):
	Tabove = temp[depth - 1]
	#print(Tabove)
	Tdepth = temp[depth]
	#print("depth " + str(Tdepth))
	Tbelow = temp[depth + 1]
	#print(Tbelow)

	return Tdepth + (1/(4*pi))*(dt/(dz**2))*(Tbelow - 2*Tdepth + Tabove)

#boolean - returns true if accurate enough
#Consider using the energy method
def isAccurate(j, surface_temp, facet_num):
	integer = floor(j/(time_steps))
	i = j
	j = j-integer*time_steps
	diff = abs(surface_temp[j+time_steps] - surface_temp[j])
	#print(diff)
	if diff <= Tacc:
		print(str(facet_num) + ": TRUE: " + str(i))
		return True
	
	return False

def RGB(T):
	Rt = R(T)
	Gt = G(T)
	Bt = B(T)

	return Rt + Gt + Bt

def R(T):
	return hex(255)

def G(T):
	G = (255/105)*(T-215)

	if G < 0:
		G = 0

	return hex(floor(G))

def B(T):
	B = (255/1225)*((T-285)**2)

	if T-285 < 0:
		B = 0;

	return hex(floor(B))
main()
# for i in range(facets):
# 	Tmean(i)
