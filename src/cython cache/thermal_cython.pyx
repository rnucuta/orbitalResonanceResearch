import numpy as np
cimport numpy as np

cpdef shadowing(position, bad_facets, all_rays, rays_obj):
  distance=np.array(position)*149598073
  indices_to_remove=bad_facets
  #self.eliminate_bad_facets()
  rays_generated=all_rays
  #self.rays_obj.generate_all_rays()
  non_shadowed_array_indices=[]
  for i in range(rays_obj.number_of_rays):
    ray_temp=[]
    for j in range(rays_obj.number_of_rays):
      if j not in indices_to_remove and j not in non_shadowed_array_indices:
        p1=rays_obj.np_asteroid_stl.vectors[j][0]+distance
        p2=rays_obj.np_asteroid_stl.vectors[j][1]+distance
        p3=rays_obj.np_asteroid_stl.vectors[j][2]+distance
        q1=rays_generated[i][:3]*1000+rays_generated[i][3:]
        q2=rays_generated[i][:3]*-1000+rays_generated[i][3:]
        if SignedVolume(q1,p1,p2,p3)*SignedVolume(q2,p1,p2,p3)<0 and np.sign(SignedVolume(q1,q2,p1,p2))==np.sign(SignedVolume(q1,q2,p2,p3))==np.sign(SignedVolume(q1,q2,p3,p1)):
          ray_temp.append(j)
    distances=[]
    for ray in ray_temp:
      distances.append(np.linalg.norm(rays_obj.centroids[ray]))
    try:
      non_shadowed_array_indices.append(ray_temp[distances.index(min(distances))])
    except:
      pass
  return non_shadowed_array_indices

cpdef SignedVolume(a,b,c,d):
  return (1.0/6.0)*np.dot(np.cross(np.subtract(b,a),np.subtract(c,a)),np.subtract(d,a))