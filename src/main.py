# from asteroid import Asteroid
# from jupiter import Jupiter

# #define intial locations for asteroid object and jupiter object

# # time_length
# # time_step

# def kirkwood():
#   #yes

# for i in range(o, time_length, time_step):
#   #yes

import numpy as np
import trimesh

import numpy as np
def SignedVolume(a,b,c,d):
	return (1.0/6.0)*np.dot(np.cross(np.subtract(b,a),np.subtract(c,a)),np.subtract(d,a))
#test

penis