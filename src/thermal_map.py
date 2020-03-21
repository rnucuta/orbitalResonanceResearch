from rays import Rays
from facets import Facets
import numpy as np

class ThermalMap:
  #thermal snapshot per time step
  def __init__(self, starting_timestep):
    self.rays_obj=Rays()
    self.copy_vectors=self.rays_obj.np_asteroid_stl.vectors
    self.normals=None
    self.timestep=starting_timestep
  def eliminate_bad_facets(self):
    distance=self.rays_obj.np_asteroid_stl.get_mass_properties()[1]
    indices_to_remove=[]
    for i in range(self.rays_obj.number_of_rays):
      if np.dot(distance, self.rays_obj.np_asteroid_stl.normals[i])<0:
        indices_to_remove.append(i)
    return indices_to_remove
  
  #shadowing code
  def shadowing(self):
    indices_to_remove=self.eliminate_bad_facets()
    rays_generated=self.rays_obj.generate_all_rays(self.rays_obj.np_asteroid_stl.get_mass_properties()[1])
    non_shadowed_array_indices=[]
    q1=self.rays_obj.np_asteroid_stl.get_mass_properties()[1]*2
    q2=self.rays_obj.np_asteroid_stl.get_mass_properties()[1]*0.05
    for i in range(self.rays_obj.number_of_rays):
      ray_temp=[]
      for j in range(self.rays_obj.number_of_rays):
        if j not in indices_to_remove and j not in non_shadowed_array_indices:
          p1=self.rays_obj.np_asteroid_stl.vectors[j][0]
          p2=self.rays_obj.np_asteroid_stl.vectors[j][0]
          p3=self.rays_obj.np_asteroid_stl.vectors[j][0]
          if SignedVolume(q1,p1,p2,p3)*SignedVolume(q1,p1,p2,p3)<0 and np.sign(SignedVolume(q1,q2,p1,p2))==np.sign(SignedVolume(q1,q2,p2,p3))==np.sign(SignedVolume(q1,q2,p3,p1)):
            ray_temp.append(j)
      distances=[]
      for ray in ray_temp:
        distances.append(np.linalg.norm(self.rays_obj.centroids[ray]))
      non_shadowed_array_indices.append(ray_temp[distances.index(min(distances))])
    return non_shadowed_array_indices
#p1,p2,p3 triangle; q1,q2 points on the line far away in both direction
    #If SignedVolume(q1,p1,p2,p3) and SignedVolume(q2,p1,p2,p3) have different signs AND SignedVolume(q1,q2,p1,p2), SignedVolume(q1,q2,p2,p3) and SignedVolume(q1,q2,p3,p1) have the same sign, then there is an intersection
  def SignedVolume(self,a,b,c,d):
    return (1.0/6.0)*np.dot(np.cross(np.subtract(b,a),np.subtract(c,a)),np.subtract(d,a))
  
  def facets_temps(self):
    pass