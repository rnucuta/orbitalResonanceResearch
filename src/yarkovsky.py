from rays import np_asteroid_stl
import numpy as np
import temp

class Yarkovsky:
  def __init__(self):
  def yarkovskyforce(self)
  emissivity = 0.73
  boltzmann = 1.38064852 * 10^(-23)
  speedoflight = 2.998 * 10^8
  forcelist = []
  temporaryforce = None
  for t in range(len(thermalmap())):
    temporaryforce = []
    for f in range(len(np_asteroid_stl.vectors)):
      facetforce = np_asteroid_stl.normals(f)*(thermalmap(t)(f))^(4) * -2 * boltzmann * emissivity / (3*speedoflight)
      temporaryforce = np.add(temporaryforce,facetforce)
    forcelist.append(temporaryforce)
  finalforce = [0,0,0]
  for x in forcelist:
    finalforce = np.add(finalforce,x)
  return np.divide(finalforce,len(thermalmap()))


  def yorptorque(self)
  torquelist = []
  temporarytorque = None
  for t in range(len(thermalmap())):
    temporarytorque = []
    for f in range(len(np_asteroid_stl.vectors)):
      centroid = np.divide(np.add(np.add(np_asteroid_stl.v0,np_asteroid_stl.v1),np_asteroid_stl.v2),3)
      facetforce = np_asteroid_stl.normals(f)*(thermalmap(t)(f))^(4) * -2 * boltzmann * emmissivity / (3*speedoflight)
      facettorque = np.cross(facetforce,centroid)
      temporarytorque = np.add(temporarytorque,facettorque)
    torquelist.append(temporarytorque)
  finaltorque = [0,0,0]
  for x in torquelist:
    finaltorque = np.add(finaltorque,x)
  return np.divide(finaltorque,len(thermalmap()))


  def phi(sunvec):
    facetlist = []
    for f in range(len(np_asteroid_stl.vectors)):
      philist = []
      for t in range(len(thermalmap())):
        philist.append(np.divide(np.dot(sunvec,np_asteroid_stl.normals(f))),(np.linalg.norm(sunvec)*np.linalg.norm(np_asteroid_stl.normals(f))))
        np_asteroid_stl.rotate(axis)
      facetlist.append(philist)
    return facetlist
