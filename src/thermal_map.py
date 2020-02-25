from rays import Rays
from facets import Facets

class ThermalMap:
  #thermal snapshot per time step
  def __init__(self):
    self.rays_obj=Rays()
    self.facets_objs=[]
  def initiate_facets_objects(self):
    for 