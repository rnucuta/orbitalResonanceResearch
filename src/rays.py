import numpy
from stl import mesh

class Rays:
  def __init__(self):
    print("rays class init")
    self.rays_array=[]
    self.np_asteroid_stl = mesh.Mesh.from_file('Steins1500.stl')
    self.number_of_rays=len(self.np_asteroid_stl.vectors)
    self.position=[-5.304365993252850*0.1*(2.668/2.647), 2.593585584222165*(2.668/2.647), 0]
  def generate_centroids(self):
    temp=[0,0,0]
    temp2=[]
    for i in range(self.number_of_rays):
        for j in range(3):
            temp[0]+=self.np_asteroid_stl.vectors[i][j][0]/3
            temp[1]+=self.np_asteroid_stl.vectors[i][j][1]/3
            temp[2]+=self.np_asteroid_stl.vectors[i][j][2]/3
        temp2.append(temp)
        temp=[0,0,0]
    return temp2

  def unit(self, vector):
    vector=numpy.array(vector)
    return vector/numpy.linalg.norm(vector)
    
  def generate_all_rays(self):
    #2-d array of length number of centroids, and stores the parametric eqn of the line for the centroids: [[a,b,c,x1,y1,z1]...]
    position=numpy.array(self.position)*149598073
    self.centroids=self.generate_centroids()+position
    for i in range(self.number_of_rays):
        n=numpy.concatenate((self.unit(self.centroids[i]),self.centroids[i]), axis=0)
        self.rays_array.append(n)
    return self.rays_array
