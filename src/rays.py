# from sympy import symbols
# x, y, z = symbols('x y z')
# import numpy as np
# import trimesh
# mesh=trimesh.load('Steins.stl')
# center_of_mass=mesh.center_mass
# import math
# from random import gauss
import numpy
from stl import mesh

class Rays:
  def __init__(self):
    # self.ast_com=center_of_mass
    # self.ast_mesh=mesh
    #need to update the number of triangles
    print("rays class init")
    self.rays_array=[]
    self.np_asteroid_stl = mesh.Mesh.from_file('Steins1000.stl')
    self.number_of_rays=len(self.np_asteroid_stl.vectors)
  # def ray_emitter(self, location_of_sun, location_of_asteroid):
    #plane of asteroid is an array of length 4: [a,b,c,d]
    #ax+by+cz=d
    #ast_radius=((3/4)*self.ast_mesh.bounding_sphere.volume*(1/math.pi))**(1/3)
    #distance_vector=np.array(location_of_asteroid)-np.array(location_of_sun)
    #unit_vector/=np.linalg.norm(list(distance_vector))
    #r(t)=(unit_vector)*t+(a,b,c)
    #the vector a,b,c has a magnitude less than ast_radius
    #return 2-d array of rays for facets class w the array
    #being[x,y,z,a,b,c]
    # temp=self.make_rand_vector(3)
    # for i in range(3):
    #   temp[i]=temp[i]*ast_radius
    # unit_vector.append(temp)
    # return unit_vector
  def generate_centroids(self):
    temp=[0,0,0]
    temp2=[]
    for i in range(self.number_of_rays):
        for j in range(3):
            temp[0]+=self.np_asteroid_stl.vectors[i][j][0]/3
            temp[1]+=self.np_asteroid_stl.vectors[i][j][1]/3
            temp[2]+=self.np_asteroid_stl.vectors[i][j][2]/3
        temp2.append(temp)
        temp=[0,0,0]
    return temp2
  def unit(self, vector):
    vector=numpy.array(vector)
    return vector/numpy.linalg.norm(vector)
  def generate_all_rays(self):
    #2-d array of length number of centroids, and stores the parametric eqn of the line for the centroids: [[a,b,c,x1,y1,z1]...]
    position=numpy.array([-0.3556267774642670,2.273733806435090,1.324572872885377])*149598073
    self.centroids=self.generate_centroids()+position
    for i in range(self.number_of_rays):
        n=numpy.concatenate((self.unit(self.centroids[i]),self.centroids[i]), axis=0)
        self.rays_array.append(n)
    return self.rays_array
