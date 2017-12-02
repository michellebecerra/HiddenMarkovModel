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


#Source: https://github.com/nickbirnberg/HMM-localisation
# https://sandipanweb.wordpress.com/2016/11/12/robot-localization-with-hmm-as-probabilistic-graphical-model/

#Parse the data 
trans_p = {}
def main():
	

	states = []
	#towers = [] #we know tower locations so no need to store
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
	
	# [start_p,emit1_p,emit2_p,emit3_p,emit4_p] = initialize(states)
	[start_p,emit_p] = initialize(states)

	# print "emit_p", obs
	# print "start_p", start_p
	# print "trans_p", trans_p
	hidden_variables = [0 for i in range(100)]
	index = 0
	for i in range(len(states)):
		for j in range(len(states)):
			string = str(i)+str(j)
			hidden_variables[index] = string
			index += 1
	hidden_variables = np.array(hidden_variables)
	# print "hidden_variables", hidden_variables
	obs_towers = ['t1','t2','t3','t4']
	viterbi(obs_towers, hidden_variables, start_p, trans_p, emit_p)
	# print trans_p
def viterbi(obs, states, start_p, trans_p, emit_p):
	V = [{}]
	for st in states:
		V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
	# print "emit_p[st][obs[0]]*start_p[st]", emit_p['43'][obs[0]]*start_p['43']
	# print "V", V
	# Run Viterbi when t > 0
	for t in range(1, len(obs)):
		V.append({})
		for st in states:
			max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
			# print trans_p['00']['22']
			# print "max_tr_prob", max_tr_prob
			for prev_st in states:
				# print prev_st
				if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
					max_prob = max_tr_prob * emit_p[st][obs[t]]

					V[t][st] = {"prob": max_prob, "prev": prev_st}
					print "st", st
					print "prev_st", prev_st
					# print V[t][st]["prev"]
					break

	# for line in dptable(V):
	# 	print line
	opt = []
	# The highest probability
	max_prob = max(value["prob"] for value in V[-1].values())
	# print V[-1].values()
	# print max_prob
	previous = None
	# Get most probable state and its backtrack
	for st, data in V[-1].items():
		if data["prob"] == max_prob:
			opt.append(st)
			previous = st
			print opt
			break
	print len(V[0])
	print range(len(V) - 2, -1, -1)
	# Follow the backtrack till the first observation
	for t in range(len(V) - 2, -1, -1):
		opt.insert(0, V[t + 1][previous]["prev"])
		previous = V[t + 1][previous]["prev"]
		print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob

def dptable(V):
	# Print a table of steps from dictionary
	yield " ".join(("%12d" % i) for i in range(len(V)))
	for state in V[0]:
		yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

	# print "V", V

def initialize(states):
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
	
	# [emit1_p,emit2_p,emit3_p,emit4_p] = emit_p(states)
	emit_p = create_emit_p(states)

	# return [start_p,emit1_p,emit2_p,emit3_p,emit4_p]
	return [start_p,emit_p]


def create_emit_p(states):
	emit_p = {}
	# emit1_p = {}
	# emit2_p = {}
	# emit3_p = {}
	# emit4_p = {}
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

	# emit1_p = collections.OrderedDict(sorted(emit1_p.items()))
	# emit2_p = collections.OrderedDict(sorted(emit2_p.items()))
	# emit3_p = collections.OrderedDict(sorted(emit3_p.items()))
	# # emit4_p = collections.OrderedDict(sorted(emit4_p.items()))
	# print "emit1_p", collections.OrderedDict(sorted(emit1_p.items()))
	# print "emit2_p", collections.OrderedDict(sorted(emit2_p.items()))
	# print "emit3_p", collections.OrderedDict(sorted(emit3_p.items()))
	# print "emit4_p", collections.OrderedDict(sorted(emit4_p.items()))

	# return [emit1_p,emit2_p,emit3_p,emit4_p]
	return emit_p

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

if __name__ == "__main__":
	main()