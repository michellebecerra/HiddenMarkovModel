# ==============Group Members==================================
# Michelle Becerra mdbecerr@usc.edu
# Amirah Anwar anwara@usc.edu
# Reetinder Kaur reetindk@usc.edu

import random
import numpy as np
import collections

# ==============Hidden Markov Models using Viterbi Algorithm==================================
#Your task is to use a Hidden Markov Model to figure out the most likely trajectory of a robot in this
#grid-world. Assume that the initial position of the robot has a uniform prior over all free cells. In each
#time-step, the robot moves to one of its four neighboring free cells chosen uniformly at random.


#Source: https://github.com/nickbirnberg/HMM-localisation
# https://sandipanweb.wordpress.com/2016/11/12/robot-localization-with-hmm-as-probabilistic-graphical-model/
#Parse the data 
trans_p = {}
def main():
	

	world = []
	#towers = [] #we know tower locations so no need to store
	noise = []
	row = []

	#load world grid into 2-D array
	with open("hmm-data.txt", 'r') as f:
		world = [line.split() for line in f.readlines()[2:12]]
	#print world
	world = np.array(world) #10x10 world grid
	
	#store noise into a 11x4 array
	with open("hmm-data.txt", 'r') as f:
		noise = [line.split() for line in f.readlines()[24:35]]
	noise = np.array(noise)
	neighbors(0,0,world)

#Observed states: Up, down, left, right
#Transition probabilites: 0.25
# Noise to towers	
#Output 
#def viterbiAlgo():
def neighbors(i, j, world):
	global trans_p
	total = 0.0
	left = False
	up = False
	right = False
	down = False

	n = len(world) - 1
	#Left
	if j - 1 >= 0:
		if world[i][j-1] == 1:
			left = True
			total += 1.0
	#Up
	if i - 1 >= 0:
		if world[i-1][j] == 1:
			up = True
			total += 1.0
	#Right
	if j + 1 <= n:
		if world[i][j+1] == 1:
			right = True
			total += 1.0

	#Down
	if  i + 1 <= n:
		if world[i+1][j] == 1:
			down = True
			total += 1.0
	
	key = str(i) + str(j)
	if key not in trans_p:
		trans_p[key] = {}


	for row in range(len(world)):
		for col in range(len(world)):
			vals = str(row) + str(col)
			if vals not in trans_p[key]:
				trans_p[key][vals] = 0.0
	
	if(left):
		trans_p[key][str(i) + str(j-1)].append(float(1.0/total))
	if(up):
		trans_p[key][str(i-1) + str(j)].append(float(1.0/total))
	if(right):
		trans_p[key][str(i) + str(j+1)].append(float(1.0/total))
	if(down):
		trans_p[key][str(i+1) + str(j)].append(float(1.0/total))
			

	print collections.OrderedDict(sorted(trans_p.items()))

if __name__ == "__main__":
	main()