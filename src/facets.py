import scipy.integrate as integrate
from rays import Rays

class facet:
  def facet_centroid(self, n):
  #for any facet n in name.stl
    #
  #take vertice vectors, average
  def __init__(self, emissitivity, facet_array):
    self.emissitivity=emissitivity
    #facet_array stores all relevant info about the facet (3 points, normal vector, location, etc)
    self.facet_array=facet_array
  def incidence_angles(self, ray_vector):
    #return angle at which a specified ray vector would hit it
  def thermal_constant(self, incidence_angles):
    #return thermal constant for a facet using the result from the incidence angles function