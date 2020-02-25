from yarkovsky import Yarkovsky
from thermal_map import ThermalMap

class Asteroid:
  def __init__(self, period, facets_array, asteroid_orientation, spin):
    self.period=period
    self.facets_array=facets_array
    self.asteroid_orientation=asteroid_orientation
    self.spin=spin
  def update_period(self, new_period):
    #probably, wrong, need a funciton to calculate new period?
    self.period=new_period
  def change_facets(self, new_facets):
    self.facets_array=new_facets
  def change_orientation(self, new_orientation):
    self.asteroid_orientation=new_orientation
  def change_spin(self, new_spin):
    self.spin=new_spin
  def orbit(self, eccentricity, angle_xy, angle_xz):
    # return array of location in space and speed and spin