import numpy as np

def similarity(x,y):

if __name__ == '__main__':
	z = [[0.53,0.85],[0.60,0.80],[-0.78,-0.62]]


	z_exp = [math.exp(i) for i in z]
	z_sum = sum(z_exp)
	z_prob = [round(i/z_sum,3) for i in z_exp ]
	all = sum(z_prob)
	print(z_prob)
	print(all)