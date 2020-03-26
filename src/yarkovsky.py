#the below line of code won't work. Wills code calls the thermal map code, which contains the stl file. You will need to import wills code, then call this file from raymo's thermal map class
from rays import np_asteroid_stl
import numpy as np
import temp
import math

class Yarkovsky:

  def orient(self):
    v = [-0.0059690746,-0.0163998975,-0.9998476952]
    itheta = math.acos(0.9998476952/np.linalg.norm(v))
    axis = np.cross([0,0,-1],v)
    np_asteroid_stl.rotate(axis,math.radians(itheta))

  def rotation(self,timesteps):
    v = [-0.0059690746,-0.0163998975,-0.9998476952]
    np_asteroid_stl.rotate(v,math.radians(360/timesteps))

  def yarkovskyforce(self):
    emissivity = 0.73
    boltzmann = 1.38064852 * 10^(-23)
    speedoflight = 2.998 * 10^8
    forcelist = []
    temporaryforce = None
    therm_map=temp.te()
    for t in range(len(therm_map)):
      temporaryforce = []
      for f in range(len(np_asteroid_stl.vectors[1])):
        facetforce = np.multiply(np_asteroid_stl.normals(f),(therm_map[t][f])**(4) * -2 * boltzmann * emissivity / (3*speedoflight))
        temporaryforce = np.add(temporaryforce,facetforce)
      forcelist.append(temporaryforce)
    finalforce = [0,0,0]
    for x in forcelist:
      finalforce = np.add(finalforce,x)
    return np.divide(finalforce,len(therm_map))

  def yorptorque(self):
    torquelist = []
    temporarytorque = None
    com = np_asteroid_stl.mass_properties()[1]
    for t in range(len(therm_map)):
      temporarytorque = []
      for f in range(len(np_asteroid_stl.vectors)):
        centroid = np.divide(np.add(np.add(np_asteroid_stl.v0,np_asteroid_stl.v1),np_asteroid_stl.v2),3)
        facetforce = np.multiply(np_asteroid_stl.normals(f),(therm_map[t][f])^(4) * -2 * boltzmann * emmissivity / (3*speedoflight))
        facettorque = np.cross(facetforce,(centroid-com))
        temporarytorque = np.add(temporarytorque,facettorque)
      torquelist.append(temporarytorque)
    finaltorque = [0,0,0]
    for x in torquelist:
      finaltorque = np.add(finaltorque,x)
    return np.divide(finaltorque,len(therm_map))

  def phi(self,position):
    orient()
    facetlist = []
    for f in range(len(np_asteroid_stl.vectors)):
      philist = []
      for t in range(len(therm_map)):
        philist.append(np.divide(np.dot(position,np_asteroid_stl.normals(f))),(np.linalg.norm(position)*np.linalg.norm(np_asteroid_stl.normals(f))))
        rotation()
      facetlist.append(philist)
    return facetlist
