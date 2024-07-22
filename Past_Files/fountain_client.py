# Files retrieved from 
# https://www.gutenberg.org/browse/scores/top
import os
import time
# import module
from datetime import datetime
import os.path
from soliton import gen_rsd_cdf #changed
from gen_matrix import G_Matrix 
from encode_mesg import encode
import soliton
 
bs = 1        # 1 byte
#bs = 128     # 128 bytes
#bs = 512     # 512 bytes
#bs = 1024    # 1 KB
#k =  4096    # 4 KB
#k =  16384   # 16 KB

def get_file_size(message_file):
    file = open(message_file)
    # get the cursor positioned at end
    file.seek(0, os.SEEK_END)
        
def chunks(file_name, size=bs):
	i=0
	message_bytes=[]

	with open(file_name, encoding='latin') as f:
	# Read two files as byte arrays
		while True:
			content = f.read(size) 
			if not content:
				break
			else:
				result_byte_array = bytearray(content, encoding='latin')
				    # Write the XORd bytes to the output file
				message_bytes.append(result_byte_array)
				i+=1
	return message_bytes


def create_file(message):
	# convert datetime obj to string
	current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
	str_current_datetime = str(current_datetime)

	# create a file object along with extension
	file_name= "mesg"+"_"+str_current_datetime+".txt"

	#file = open('/home/seed/Documents/Messages/%s' %file_name, 'w')
	file = open('/tmp/Client/Messages/%s' %file_name, 'w')
	file.close()

	#path = '/home/seed/Documents/Messages/'
	path = '/tmp/Client/Messages/'
	message_file = path+file_name

	with open(file.name, "w", newline='') as f:
		f.write(message)

	with open(file.name, "r") as f:
		for line in f:
			line = line.rstrip('\r\n') # strip out all tailing whitespace

	return message_file

def generate_message(message):
	mesg_file =  create_file(message)
	get_file_size(mesg_file)
	blocks = chunks(mesg_file)
	K = len(blocks)

	seed, c, delta = soliton.seed, soliton.PRNG_C, soliton.PRNG_DELTA
	prng = soliton.PRNG(params=(K, delta, c))
	prng.set_seed(seed)

	probs = gen_rsd_cdf(K, delta, c)
	G = G_Matrix(K, probs)
	droplets = encode(G, blocks, K, bs) #encoded_message
	return (K, droplets)
	
