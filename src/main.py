#IMPORT yarkovsky.py

def save_yark_vector(np_vec):
	with open('final_yark_vector.txt', 'w') as f:
    	for item in list(np_vec):
        	f.write("%s\n" % item)