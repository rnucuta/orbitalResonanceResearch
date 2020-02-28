from rays import Rays
from facets import Facets
import numpy as np

class ThermalMap:
  #thermal snapshot per time step
  def __init__(self, timestep):
    self.rays_obj=Rays()
    self.copy_vectors=self.rays_obj.np_asteroid_stl.vectors
    self.normals=None
    self.timestep=timestep
  def eliminate_bad_facets(self):
  	distance=self.rays_obj.np_asteroid_stl.get_mass_properties()[1]
  	indices_to_remove=[]
  	for i in range(len(self.rays_obj.np_asteroid_stl.normals)):
  		if np.dot(distance, self.rays_obj.np_asteroid_stl.normals[i])<0:
  			indices_to_remove.append(i)
  	return indices_to_remove
  def shadowing(self):
  	pass
  def facets_temps():
  	pass
  def SignedVolume(a,b,c,d):
	return (1.0/6.0)*np.dot(np.cross(np.subtract(b,a),np.subtract(c,a)),np.subtract(d,a))