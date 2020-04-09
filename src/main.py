import time
import datetime
start = time.time()
#IMPORT yarkovsky.py
from yarkovsky import Yarkovsky
print('Making Yarkovsky object')
yarkovsky_obj=Yarkovsky()

print('Running yarkovskyforce function')
vector_answer=yarkovsky_obj.yarkovskyforce()
torque_answer = yarkovsky_obj.yorptorque()
def save_yark_vector(np_vec, np_vec2):
	with open('final_yark_vector.txt', 'w') as f:
		for item in list(np_vec):
			f.write("%s\n" % item)
		f.write("\n")
		for item in list(np_vec2):
			f.write("%s\n" % item)
print("================================================================")
print("Vector answer: {}".format(vector_answer))
print("================================================================")
print("Torque answer: {}".format(torque_answer))
print("================================================================")
save_yark_vector(vector_answer, torque_answer)

end = time.time()
print("time: " + str(datetime.timedelta(seconds=end-start)))