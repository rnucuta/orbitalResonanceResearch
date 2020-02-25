from thermal import thermal
class Yarkovsky:
  def crossProd(a,b):
      dimension = len(a)
      c = []
      for i in range(dimension):
        c.append(0)
        for j in range(dimension):
          if j <> i:
            for k in range(dimension):
              if k <> i:
                if k > j:
                  c[i] += a[j]*b[k]
                elif k < j:
                  c[i] -= a[j]*b[k]
      return c
  k=-(2*5.67 * 10^-8)/(3*2.998*10^8)
   #def __init__(self):
     #ang_v=something
     #sont need, see astroid class?
    #i honestly don't know math behind this shit/initial stuff to keep in mind
  def force_vectors(self):
    f= k*eccentricity*sum(thermal^4*normal_vectors)
    #f=c*integrate(emissitivity*T^4*normal)
    #return force vectors on asteroid
    return f
  def torque_vectors(self):
    tor= k*eccentricity*sum(thermal^4*crossProd((facet_centroid_center_of_mass),normal_vectors)
    #take cross product of radius from com to facet centroid
    #return torque vectors on asteroid
    return tor
  def spin(self):
    #return YORP spin effects on asteroid
    #do initial condition plus timestep effects and then set them as new initial (how tf do u do that)
    #IF YOU SEE THIS COMMENT, TELL US THAT UR DOING WORK
    #im working homie damn, i got home saturday evening