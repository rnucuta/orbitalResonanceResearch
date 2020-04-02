import copy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from sympy import solve
from sympy import Symbol
from math import *
#from stl_editor import angles, facetNumber, shadows
from thermal_map import ThermalMap

#constants
class Temperature:
	#print(feta[0][3])
	def __init__(self, Tacc, time_steps, depth_steps):
		self.thermalmap_obj = ThermalMap()
		self.Tacc = Tacc
		self.time_steps = time_steps
		self.depth_steps = depth_steps
		self.P = 21768.516 #period of rotation(spin)(seconds)
		self.gamma = 110 #sqrt(k*rho*C) thermal inertia
		self.k = 4.5 #thermal conductivity #UNKNOWN
		self.rho = 1800#density #UNKNOWN
		self.C = (self.gamma**2)/(self.k*self.rho)#specific heat capacity #UNKNOWN
		self.E = 0.7 #emissivity
		self.S = 5.67 * (10**-8)#Stefan–Boltzmann constant
		self.Wsun = 1367 #Power from sun (Wsun/(rh)^2)(W/m^2)
		self.Ab = 0.24 #Bond Albedo
		self.z = sqrt((4*pi*self.P*self.k)/(self.rho*self.C)) #normalized depth
		self.t = self.P #normalized time

		#Things to be determined
		self.r = np.linalg.norm(self.thermalmap_obj.position) #distance from Sun(AU)
		#500
		#300
		self.facets = self.thermalmap_obj.rays_obj.number_of_rays #number of facets
		self.feta = self.thermalmap_obj.phi(time_steps) #si(t), feta(feta) #2d array #UNKNOWN


		#####
		#WILL CALL THE ORIENT FUNCTION HERE
		###


		self.shadow = self.thermalmap_obj.shadowing() #1-not shadowed 0-shadowed #2d array #UNKNOWN
		# print(feta)
		# print(shadow)
		self.dz = 2/self.depth_steps #change in z #0-depth_steps-1
		self.dt = 1/self.time_steps #change in t #0-time_steps-1

	def temp(self):
		#initialize
		final_temps = [[0 for k in range(self.facets)] for i in range(self.time_steps)] #timesteps by facets
		temp = [[0 for k in range(self.depth_steps)] for i in range(self.facets)] #facet by depth
		#temp_temporary = [0 for i in range(depth_steps)]
		#for calculating accuracy
		surface_temp = [0 for j in range(2*self.time_steps)] #temp of top depth for each time for one facet
		#time = 0

		#for facets
		for facet_num in range(self.facets):
			#initialize temperatures
			j = 0 #time
			temp_temporary = self.setTemp(facet_num)
			temp[facet_num] = temp_temporary[:]
			
			#until accurate repeat facet
			while j < 10*self.time_steps or not self.isAccurate(j, surface_temp, facet_num):
				integer = floor(j/(2*self.time_steps))
				time = j - self.time_steps*floor(j/self.time_steps)
				#test
				# if j > time_steps:
				# 	break
				#test

				#storing previous temps
				if j < self.time_steps:
					surface_temp[j] = temp[facet_num][0]
				else:
					#integer = floor(j/(2*time_steps))
					surface_temp[j-integer*2*self.time_steps] = temp[facet_num][0]

				#for depth steps
				for i in range(self.depth_steps):
					#top
					if i == 0:
						temp_temporary[i] = self.solveExternalBC(facet_num, j, temp_temporary)
						continue

					#bottom
					if i == self.depth_steps-1:
						#This assigns a reference but technically that doesnt matter
						temp_temporary[i] = temp_temporary[i-1]
						continue

					#everything else
					temp_temporary[i] = self.solveDepthTemp(facet_num, i, temp_temporary)

				#set temps
				temp[facet_num] = temp_temporary[:]

				
				final_temps[time][facet_num] = temp[facet_num][0]
				#change time
				j += 1
				#print(j)
			print(str(facet_num) + ": hey")
		
		# for i in final_temps:
			#print(i)
		print(final_temps[0])
		return final_temps




		# hexes = []
		# for i in range(facets):
		# 	T = final_temps[0][i]
		# 	value = RGB(T)
		# 	hexes.append(value)

		# for i in hexes:
		# 	print(i)
						
	#calculates Tmean for a facet
	def Tmean(self, facet_num): 
		Fsun = self.Wsun/(self.r**2)
		constant = ((Fsun*(1-self.Ab)/(self.E*self.S))**(1/4))
		sums = 0
		for j in range(self.time_steps):
			if self.shadow.contains(j):
				shade = 1
			else:
				shade = 0
			angle = self.feta[facet_num][j]
			#print(angle)
			
			sums += ((shade*abs(angle))**(1/4))*self.dt
		return (constant*(sums))/1

	#assigns an initial temperature to all depth steps for a facet
	def setTemp(self, facet_num):
		temperature = [0 for j in range(self.depth_steps)]
		mean = self.Tmean(facet_num)
		for i in range(self.depth_steps):
			Ti = 1.7*mean#*(exp(-2*pi*i*dz))
			temperature[i] = Ti

		#print(temperature)
		return temperature

	#solves external BC, returns temp
	def solveExternalBC(self, facet_num, j, temp):
		integer = floor(j/(self.time_steps))
		j = j-integer*self.time_steps
		if self.shadow.contains(j):
			shade = 1
		else:
			shade = 0
		angle = self.feta[facet_num][j]
		Fsun = self.Wsun/(self.r**2)
		T1 = temp[1];
		# print(shade)
		# print(T1)
		#T = Symbol('T')
		#solution = solve((1-Ab)*shade*angle*Fsun + (gamma/(sqrt(4*pi*P)))*((T1-T)/dz) - E*S*(T**4), T)
		coeff = [-self.E*self.S, 0, 0, -(self.gamma/(sqrt(4*pi*self.P)*self.dz)), (1-self.Ab)*shade*angle*Fsun + (self.gamma/(sqrt(4*pi*self.P)*self.dz))*T1]
		solution  = np.roots(coeff)
		#print(solution)
		for i in solution:
			if np.isreal(i) and i > 0:
				#print("real" + str(np.real(i)))
				return np.real(i)

		# print(solution)
		# return solution
	#solve temperature for depth steps
	def solveDepthTemp(self, facet_num, depth, temp):
		Tabove = temp[depth - 1]
		#print(Tabove)
		Tdepth = temp[depth]
		#print("depth " + str(Tdepth))
		Tbelow = temp[depth + 1]
		#print(Tbelow)

		final = Tdepth + (1/(4*pi))*(self.dt/(self.dz**2))*(Tbelow - 2*Tdepth + Tabove)
		# if final < 0:
		# 	final = 0

		return abs(final)

	#boolean - returns true if accurate enough
	#Consider using the energy method
	def isAccurate(self, j, surface_temp, facet_num):
		integer = floor(j/(self.time_steps))
		i = j
		j = j-integer*self.time_steps
		diff = abs(surface_temp[j+self.time_steps] - surface_temp[j])
		#print(diff)
		if diff <= self.Tacc:
			print(str(facet_num) + ": TRUE: " + str(i))
			print(surface_temp[j])
			return True
		
		return False

	# def RGB(self, T):
	# 	Rt = R(T)
	# 	Gt = G(T)
	# 	Bt = B(T)

	# 	return str(Rt) + str(Gt) + str(Bt)

	# def R(self,T):
	# 	return hex(255)

	# def G(self,T):
	# 	G = (255/105)*(T-215)

	# 	if G < 0:
	# 		G = 0

	# 	return hex(floor(G))

	# def B(self,T):
	# 	B = (255/1225)*((T-285)**2)

	# 	if T-285 < 0:
	# 		B = 0;

	# 	return hex(floor(B))
	#te()
	# for i in range(facets):
	# 	Tmean(i)
