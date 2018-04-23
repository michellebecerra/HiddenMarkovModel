# HiddenMarkovModel
Hidden Markov Model to determine the most probable path of a robot given a terrain.

The world is denoted by a 10-by-10 2d grid located in hmm-data.txt. 
Free celss are represented as 1's and the obstacles are represented as 0's. 
Using the Viterbi Algorithm we figure out the most likely trajectory of a robot in this grid world. 
Assuming the intial positon of the robot has a uniform priori over all free cells and at each time-step, 
the robot moves to one of its four neighboring free cells chosen uniformly at random.

To run:
python hmm.py
