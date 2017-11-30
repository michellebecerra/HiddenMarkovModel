# ==============Group Members==================================
# Michelle Becerra mdbecerr@usc.edu
# Amirah Anwar anwara@usc.edu
# Reetinder Kaur reetindk@usc.edu

import random
import numpy as np

# ==============Hidden Markov Models using Viterbi Algorithm==================================

#Parse the data 
def main():
	
	world = []
	#towers = [] #we know tower locations so no need to store
	noise = []
	row = []

	#load world grid into 2-D array
	with open("hmm-data.txt", 'r') as f:
		world = [line.split() for line in f.readlines()[2:12]]
	world = np.array(world) #10x10 world grid
	
	#store noise into a 11x4 array
	with open("hmm-data.txt", 'r') as f:
		noise = [line.split() for line in f.readlines()[24:35]]
	noise = np.array(noise)
	

	


	
	


if __name__ == "__main__":
	main()