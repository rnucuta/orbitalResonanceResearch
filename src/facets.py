import scipy.integrate as integrate
from rays import Rays

class facet:
  def __init__(self, facet_cords, facet_normal):
    self.shadowing=False
    self.cords=facet_cords
    self.normal=facet_normal
  #take vertice vectors, average
  