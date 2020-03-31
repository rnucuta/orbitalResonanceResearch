#the below line of code won't work. Wills code calls the thermal map code, which contains the stl file. You will need to import wills code, then call this file from raymo's thermal map class
from temp import Temperature
import numpy as np
import temp
import math

class Yarkovsky:
  def __init__(self):
    self.Temperature=Temperature(0.01, 400, 50)
    self.np_asteroid_stl=self.Temperature.thermalmap_obj.rays_obj.np_asteroid_stl

  def yarkovskyforce(self):
    emissivity = 0.73
    boltzmann = 1.38064852 * 10^(-23)
    speedoflight = 2.998 * 10^8
    forcelist = []
    temporaryforce = None
    therm_map=temp.te()
    for t in range(len(therm_map)):
      temporaryforce = []
      for f in range(len(self.np_asteroid_stl.vectors[1])):
        facetforce = np.multiply(self.np_asteroid_stl.normals(f),(therm_map[t][f])**(4) * -2 * boltzmann * emissivity / (3*speedoflight))
        temporaryforce = np.add(temporaryforce,facetforce)
      forcelist.append(temporaryforce)
    finalforce = [0,0,0]
    for x in forcelist:
      finalforce = np.add(finalforce,x)
    return np.divide(finalforce,len(therm_map))

  def yorptorque(self):
    torquelist = []
    temporarytorque = None
    com = self.np_asteroid_stl.mass_properties()[1]
    for t in range(len(therm_map)):
      temporarytorque = []
      for f in range(len(self.np_asteroid_stl.vectors)):
        centroid = np.divide(np.add(np.add(self.np_asteroid_stl.v0,self.np_asteroid_stl.v1),self.np_asteroid_stl.v2),3)
        facetforce = np.multiply(self.np_asteroid_stl.normals(f),(therm_map[t][f])^(4) * -2 * boltzmann * emmissivity / (3*speedoflight))
        facettorque = np.cross(facetforce,(centroid-com))
        temporarytorque = np.add(temporarytorque,facettorque)
      torquelist.append(temporarytorque)
    finaltorque = [0,0,0]
    for x in torquelist:
      finaltorque = np.add(finaltorque,x)
    return np.divide(finaltorque,len(therm_map))