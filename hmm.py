# ==============Group Members==================================
# Michelle Becerra mdbecerr@usc.edu
# Amirah Anwar anwara@usc.edu
# Reetinder Kaur reetindk@usc.edu

import random
import numpy as np
from scipy.spatial import distance
import collections

# ==============Hidden Markov Models using Viterbi Algorithm==================================
trans_p = {}
#Parse the data 
def main():
	
	states = []
	#towers = [] #we know tower locations so no need to store
	obs = []
	start_p = []
	#load states grid into 2-D array
	with open("hmm-data.txt", 'r') as f:
		states = [np.array(map(int,line.split())) for line in f.readlines()[2:12]]
	states = np.array(states) #10x10 states grid
	
	#store obs into a 11x4 array
	with open("hmm-data.txt", 'r') as f:
		obs = [np.array(map(float,line.split())) for line in f.readlines()[24:35]]
	obs = np.array(obs)
	
	print "states", states

	[start_p,emit1_p,emit2_p,emit3_p,emit4_p] = initialize(states)
	print trans_p

def initialize(states):
	start_p = np.zeros(states.shape)
	n = len(states)
	for i in range(n):
		for j in range(n):
			#Create start_p
			if(states[i][j] == 1):
				start_p[i][j] = 1.0/87.0
				neighbors(i,j,states)
			else:
				start_p[i][j] = 0.0
	
	[emit1_p,emit2_p,emit3_p,emit4_p] = emit_p(states)
	return [start_p,emit1_p,emit2_p,emit3_p,emit4_p]


def emit_p(states):
	emit1_p = {}
	emit2_p = {}
	emit3_p = {}
	emit4_p = {}
	for i in range(len(states)):
		for j in range(len(states)):
			if states[i][j] != 0:
				[d1,d2,d3,d4] = eucl_dist(np.array((i,j)))
				range1 =  np.arange(0.7*d1, 1.3*d1, 0.1)
				range2 =  np.arange(0.7*d2, 1.3*d2, 0.1)
				range3 =  np.arange(0.7*d3, 1.3*d3, 0.1)
				range4 =  np.arange(0.7*d4, 1.3*d4, 0.1)
			else:
				range1 =  np.array([])
				range2 =  np.array([])
				range3 =  np.array([])
				range4 =  np.array([])

			# print "range1,range2,range3,range4", len(range1),len(range2),len(range3),len(range4)
			# print "len(range1)", len(range1)
			if len(range1) != 0:
				emit1_p[str(i)+str(j)] = float(1.0/len(range1))
			else:
				emit1_p[str(i)+str(j)] = 0.0
			# print "len(range2)", len(range2)
			if len(range2) != 0:
				emit2_p[str(i)+str(j)] = float(1.0/len(range2))
			else:
				emit2_p[str(i)+str(j)] = 0.0
			# print "len(range3)", len(range3)
			if len(range3) != 0:
				emit3_p[str(i)+str(j)] = float(1.0/len(range3))
			else:
				emit3_p[str(i)+str(j)] = 0.0
			# print "len(range4)", len(range4)
			if len(range4) != 0:
				emit4_p[str(i)+str(j)] = float(1.0/len(range4))
			else:
				emit4_p[str(i)+str(j)] = 0.0

	# emit1_p = collections.OrderedDict(sorted(emit1_p.items()))
	# emit2_p = collections.OrderedDict(sorted(emit2_p.items()))
	# emit3_p = collections.OrderedDict(sorted(emit3_p.items()))
	# # emit4_p = collections.OrderedDict(sorted(emit4_p.items()))
	# print "emit1_p", collections.OrderedDict(sorted(emit1_p.items()))
	# print "emit2_p", collections.OrderedDict(sorted(emit2_p.items()))
	# print "emit3_p", collections.OrderedDict(sorted(emit3_p.items()))
	# print "emit4_p", collections.OrderedDict(sorted(emit4_p.items()))

	return [emit1_p,emit2_p,emit3_p,emit4_p]



def eucl_dist(coord):
	tower1 = np.array((0,0))
	tower2 = np.array((0,9))
	tower3 = np.array((9,0))
	tower4 = np.array((9,9))

	d1 = distance.euclidean(tower1,coord)
	d2 = distance.euclidean(tower2,coord)
	d3 = distance.euclidean(tower3,coord)
	d4 = distance.euclidean(tower4,coord)

	return [d1,d2,d3,d4]

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
		trans_p[key][str(i) + str(j-1)] = (float(1.0/total))
	if(up):
		trans_p[key][str(i-1) + str(j)] = (float(1.0/total))
	if(right):
		trans_p[key][str(i) + str(j+1)] = 9.9
		trans_p[key][str(i) + str(j+1)] = (float(1.0/total))
	if(down):
		trans_p[key][str(i+1) + str(j)] = (float(1.0/total))
			

	print collections.OrderedDict(sorted(trans_p.items()))

if __name__ == "__main__":
	main()