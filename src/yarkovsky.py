#the below line of code won't work. Wills code calls the thermal map code, which contains the stl file. You will need to import wills code, then call this file from raymo's thermal map class
from temp import Temperature
import numpy as np
import temp
import math
import pickle

class Yarkovsky:
  def __init__(self):
    print("Yark init")
    self.load_temp=True
    self.Temperature=None
    self.therm_map=None
    if not self.load_temp:
      self.Temperature=Temperature(0.01, 400, 50)
      self.therm_map= self.Temperature.temp()
      with open('./temp_obj.obj', 'wb') as f:
        pickle.dump(self.Temperature, f)
    else:
      with open('./temp_obj.obj', 'rb') as f:
        self.Temperature=pickle.load(f)
      self.therm_map=self.Temperature.final_temps
    self.np_asteroid_stl=self.Temperature.thermalmap_obj.rays_obj.np_asteroid_stl
    

  def yarkovskyforce(self):
    print("Yarkovsky initiated")
    emissivity = 0.73
    boltzmann = 5.670374 * (10**(-8))
    speedoflight = 2.998 * (10**8)
    forcelist = []
    temporaryforce = None
    print("Yarkovsky variables instantiated")
    for t in range(len(self.therm_map)):
      temporaryforce = np.zeros(3)
      for f in range(len(self.np_asteroid_stl.vectors)):
        a = self.np_asteroid_stl.vectors[f][0]
        b = self.np_asteroid_stl.vectors[f][1]
        c = self.np_asteroid_stl.vectors[f][2]
        ds = abs(np.cross(np.subtract(b,a),np.subtract(c,a))) / 2
        facetforce = np.multiply(self.np_asteroid_stl.normals[f],(self.therm_map[t][f])**(4) * -2 * boltzmann * emissivity * ds / (3*speedoflight))
        temporaryforce = np.add(temporaryforce,facetforce)
      forcelist.append(temporaryforce)
    finalforce = [0,0,0]
    print("Iteration Successful")
    for x in forcelist:
      finalforce = np.add(finalforce,x)
    return np.divide(finalforce,len(self.therm_map))
    print("Yarkovsky force Successful")

  def yorptorque(self):
    print("YORP Torque initiated")
    torquelist = []
    temporarytorque = None
    com = self.np_asteroid_stl.mass_properties()[1]
    ds = math.sqrt(3) * (1000 * np.linalg.norm(np.subtract(self.np_asteroid_stl.vectors[1][2],self.np_asteroid_stl.vectors[1][1])))**(2) / 4
    emissivity = 0.73
    boltzmann = 1.38064852 * (10**(-23))
    speedoflight = 2.998 * (10**8)
    print("YORP variables instantiated")
    for t in range(len(self.therm_map)):
      temporarytorque = []
      for f in range(len(self.np_asteroid_stl.vectors)):
        a = self.np_asteroid_stl.vectors[f][1]
        b = self.np_asteroid_stl.vectors[f][2]
        c = self.np_asteroid_stl.vectors[f][3]
        ds = abs(np.cross(np.subtract(b,a),np.subtract(c,a))) / 2
        centroid = np.divide(np.add(np.add(self.np_asteroid_stl.v0[f],self.np_asteroid_stl.v1[f]),self.np_asteroid_stl.v2[f]),3)
        facetforce = np.multiply(self.np_asteroid_stl.normals[f],(self.therm_map[t][f])**(4) * -2 * boltzmann * emmissivity * ds / (3*speedoflight))
        facettorque = np.cross(facetforce,(centroid-com))
        temporarytorque = np.add(temporarytorque,facettorque)
      torquelist.append(temporarytorque)
    finaltorque = [0,0,0]
    print("YORP Iteration Successful")
    for x in torquelist:
      finaltorque = np.add(finaltorque,x)
    return np.divide(finaltorque,len(self.therm_map))
    print("YORP Torque Successful")
