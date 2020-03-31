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
	def __init__(self, Tacc, r, time_steps, depth_steps):
		self.thermalmap_obj = ThermalMap()
		self.Tacc = Tacc
		self.r = r
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
		self.r = r #distance from Sun(AU)
		#500
		#300
		self.depth_steps = depth_steps #number of depth steps
		self.time_steps = time_steps #number of time steps
		self.facets = self.thermalmap_obj.rays_obj.number_of_rays #number of facets
		self.feta = self.thermalmap_obj.phi(position) #si(t), feta(feta) #2d array #UNKNOWN


		#####
		#WILL CALL THE ORIENT FUNCTION HERE
		###


		self.shadow = self.thermalmap_obj.shadowing() #1-not shadowed 0-shadowed #2d array #UNKNOWN
		# print(feta)
		# print(shadow)
		self.dz = 2/self.depth_steps #change in z #0-depth_steps-1
		self.dt = 1/self.time_steps #change in t #0-time_steps-1
		self.Tacc = Tacc #min change in T #UNKNOWN

	def temp(self.):
		#initialize
		final_temps = [[0 for k in range(facets)] for i in range(time_steps)] #timesteps by facets
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
			while j < 10*time_steps or not isAccurate(j, surface_temp, facet_num):
				integer = floor(j/(2*time_steps))
				time = j - time_steps*floor(j/time_steps)
				#test
				# if j > time_steps:
				# 	break
				#test

				#storing previous temps
				if j < time_steps:
					surface_temp[j] = temp[facet_num][0]
				else:
					#integer = floor(j/(2*time_steps))
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

				
				final_temps[time][facet_num] = temp[facet_num][0]
				#change time
				j += 1
				#print(j)
			#print(str(facet_num) + ": hey")
		
		for i in final_temps:
			print(i)

		return final_temps




		# hexes = []
		# for i in range(facets):
		# 	T = final_temps[0][i]
		# 	value = RGB(T)
		# 	hexes.append(value)

		# for i in hexes:
		# 	print(i)
						
	#calculates Tmean for a facet
	def Tmean(self,facet_num): 
		constant = (((1-Ab)/(E*S))**(1/4))
		sums = 0
		for j in range(time_steps):
			shade = shadow[facet_num][j]
			angle = feta[facet_num][j]
			#print(angle)
			Fsun = Wsun/(r*r)
			sums += (shade*abs(angle)*Fsun)*dt
		#print(constant*((sums)**(1/4))/1)
		return (constant*((sums)**(1/4)))/1

	#assigns an initial temperature to all depth steps for a facet
	def setTemp(self,facet_num):
		temperature = [0 for j in range(depth_steps)]
		mean = Tmean(facet_num)
		for i in range(depth_steps):
			Ti = mean#*(exp(-2*pi*i*dz))
			temperature[i] = Ti

		#print(temperature)
		return temperature

	#solves external BC, returns temp
	def solveExternalBC(self,facet_num, j, temp):
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
		#print(solution)
		for i in solution:
			if np.isreal(i) and i > 0:
				#print("real" + str(np.real(i)))
				return np.real(i)

		# print(solution)
		# return solution
	#solve temperature for depth steps
	def solveDepthTemp(self,facet_num, depth, temp):
		Tabove = temp[depth - 1]
		#print(Tabove)
		Tdepth = temp[depth]
		#print("depth " + str(Tdepth))
		Tbelow = temp[depth + 1]
		#print(Tbelow)

		final = Tdepth + (1/(4*pi))*(dt/(dz**2))*(Tbelow - 2*Tdepth + Tabove)
		# if final < 0:
		# 	final = 0

		return abs(final)

	#boolean - returns true if accurate enough
	#Consider using the energy method
	def isAccurate(self,j, surface_temp, facet_num):
		integer = floor(j/(time_steps))
		i = j
		j = j-integer*time_steps
		diff = abs(surface_temp[j+time_steps] - surface_temp[j])
		#print(diff)
		if diff <= Tacc:
			print(str(facet_num) + ": TRUE: " + str(i))
			print(surface_temp[j])
			return True
		
		return False

	def RGB(self,T):
		Rt = R(T)
		Gt = G(T)
		Bt = B(T)

		return str(Rt) + str(Gt) + str(Bt)

	def R(self,T):
		return hex(255)

	def G(self,T):
		G = (255/105)*(T-215)

		if G < 0:
			G = 0

		return hex(floor(G))

	def B(self,T):
		B = (255/1225)*((T-285)**2)

		if T-285 < 0:
			B = 0;

		return hex(floor(B))
	#te()
	# for i in range(facets):
	# 	Tmean(i)
