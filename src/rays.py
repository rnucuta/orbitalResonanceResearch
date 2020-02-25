from sympy import symbols
x, y, z = symbols('x y z')
import numpy as np
import trimesh
mesh=trimesh.load('Steins.stl')
center_of_mass=mesh.center_mass
import math
from random import gauss
import numpy
from stl import mesh

class Rays:
  def __init__(self):
    self.ast_com=center_of_mass
    self.ast_mesh=mesh
    #need to update the number of triangles
    self.number_of_rays=1.5*20480
    self.rays_array=[]
    self.np_asteroid_stl = mesh.Mesh.from_file('Steins.stl')
  def make_rand_vector(self,dims):
    vec = [gauss(0, 1) for i in range(dims)]
    mag = sum(x**2 for x in vec) ** .5
    return [x/mag for x in vec]
  def ray_emitter(self, location_of_sun, location_of_asteroid):
    #plane of asteroid is an array of length 4: [a,b,c,d]
    #ax+by+cz=d
    ast_radius=((3/4)*self.ast_mesh.bounding_sphere.volume*(1/math.pi))**(1/3)
    distance_vector=np.array(location_of_asteroid)-np.array(location_of_sun)
    unit_vector/=np.linalg.norm(list(distance_vector))
    #r(t)=(unit_vector)*t+(a,b,c)
    #the vector a,b,c has a magnitude less than ast_radius
    #return 2-d array of rays for facets class w the array
    #being[x,y,z,a,b,c]
    temp=self.make_rand_vector(3)
    for i in range(3):
      temp[i]=temp[i]*ast_radius
    unit_vector.append(temp)
    return unit_vector
  def generate_all_rays(self, location_of_asteroid):
    for i in range(self.number_of_rays):
      self.rays_array.append(self.ray_emitter([0,0,0], location_of_asteroid))
    return self.rays_array