# ==============Group Members==================================
# Michelle Becerra mdbecerr@usc.edu
# Amirah Anwar anwara@usc.edu
# Reetinder Kaur reetindk@usc.edu

import random
import numpy as np
from scipy.spatial import distance
import collections

# ==============Hidden Markov Models using Viterbi Algorithm==================================
#Your task is to use a Hidden Markov Model to figure out the most likely trajectory of a robot in this
#grid-world. Assume that the initial position of the robot has a uniform prior over all free cells. In each
#time-step, the robot moves to one of its four neighboring free cells chosen uniformly at random.

#Parse the data 
trans_p = collections.OrderedDict({})
def main():
	states = []
	obs = []
	start_p = []
	emit_p = {}
	#load states grid into 2-D array
	with open("hmm-data.txt", 'r') as f:
		states = [np.array(map(int,line.split())) for line in f.readlines()[2:12]]
	states = np.array(states) #10x10 states grid
	
	#store obs into a 11x4 array
	with open("hmm-data.txt", 'r') as f:
		obs = [np.array(map(float,line.split())) for line in f.readlines()[24:35]]
	obs = np.array(obs)
	
	[start_p,emit_p,hidden_variables] = initialize(states, obs)

	obs_towers = ['t1','t2','t3','t4']

	viterbi(obs_towers, hidden_variables, start_p, trans_p, emit_p)
	print hidden_variables

def viterbi(obs, states, start_p, trans_p, emit_p):
	V = [{}]

	for point in states[0]:
		V[0][point] = {"prob": start_p[point], "prev": None}

	for t in range(1, 11):
		V.append({})
		for st in states[t-1]:
			if st in trans_p[st]:
				for state in trans_p[st]:
					if state in states[t]:
						if state not in V[t]:
							V[t][state] = {"prob": 0.0, "prev": None}
							V[t][state]["prob"] = V[t-1][st]["prob"]*trans_p[state][st]
							V[t][state]["prev"] = st
						else:
							if V[t-1][st]["prob"]*trans_p[state][st] > V[t][state]["prob"]:
								V[t][state]["prob"] = V[t-1][st]["prob"]*trans_p[state][st]
								V[t][state]["prev"] = st

	max_point = ''
	max_prob = -1
	for point in V[10]:
		if V[10][point]["prob"] > max_prob:
			max_prob = V[10][point]["prob"]
			max_point = point

	probable_path = []
	probable_path.append(max_point)
	for i in range(10,0,-1):
		max_point = V[i][max_point]["prev"]
		probable_path.insert(0, max_point)

	path = ""
	for point in probable_path:
		path += "(" + str(int(point)/10) + "," + str(int(point)%10) + ")" + "->"

	path = path[:-2]
	print "The most likely trajectory of the robot for 11 time-steps:\n", path

def initialize(states, obs):
	start_p = {}
	emit_p = {}
	n = len(states)
	for i in range(n):
		for j in range(n):
			key = str(i)+str(j)
			neighbors(i,j,states)
			if key not in start_p:
				#Create start_p
				if(states[i][j] == 1):
					start_p[str(i)+str(j)] = 1.0/87.0
				else:
					start_p[str(i)+str(j)] = 0.0
	
	[emit_p, hidden_variables] = create_emit_p(states, obs)

	return [start_p,emit_p,hidden_variables]

def create_emit_p(states, obs):
	emit_p = {}
	hidden_variables = {}
	d1 = 0.0
	d2 = 0.0
	d3 = 0.0
	d4 = 0.0

	for init in range(11):
		hidden_variables[init] = []

	for i in range(len(states)):
		for j in range(len(states)):
			# print hidden_variables
			if states[i][j] != 0:
				[d1,d2,d3,d4] = eucl_dist(np.array((i,j)))
				range1 =  np.arange(0.7*d1, 1.3*d1, 0.1)
				range2 =  np.arange(0.7*d2, 1.3*d2, 0.1)
				range3 =  np.arange(0.7*d3, 1.3*d3, 0.1)
				range4 =  np.arange(0.7*d4, 1.3*d4, 0.1)

				#eliminate states based on noisy distances to towers
				val = str(i)+str(j)
				for row in range(11):
					if 0.7*d1 <= obs[row][0] <= 1.3*d1 and 0.7*d2 <= obs[row][1] <= 1.3*d2 and 0.7*d3 <= obs[row][2] <= 1.3*d3 and 0.7*d4 <= obs[row][3] <= 1.3*d4:
						hidden_variables[row].append(val)
			else:
				range1 =  np.array([])
				range2 =  np.array([])
				range3 =  np.array([])
				range4 =  np.array([])


			key = str(i)+str(j)
			if key not in emit_p:
				emit_p[key] = {'t1' : 0.0, 't2': 0.0, 't3' : 0.0, 't4' : 0.0}

			if len(range1) != 0:
				emit_p[key]['t1'] = float(1.0/len(range1))
			if len(range2) != 0:
				emit_p[key]['t2'] = float(1.0/len(range2))
			if len(range3) != 0:
				emit_p[key]['t3'] = float(1.0/len(range3))
			if len(range4) != 0:
				emit_p[key]['t4'] = float(1.0/len(range4))

	return [emit_p, hidden_variables]

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
		trans_p[key] = collections.OrderedDict({})


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
	
	print trans_p['00']
if __name__ == "__main__":
	main()