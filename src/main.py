#IMPORT yarkovsky.py
from yarkovsky import Yarkovsky

yarkovsky_obj=Yarkovsky()

def save_yark_vector(np_vec):
	with open('final_yark_vector.txt', 'w') as f:
    	for item in list(np_vec):
        	f.write("%s\n" % item)

vector_answer=yarkovsky_obj.yarkovskyforce()
save_yark_vector(vector_answer)