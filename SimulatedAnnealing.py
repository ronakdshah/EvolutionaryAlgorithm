import numpy as np

def temperature(t,i):
	return t/(1.0+np.log(i+1))
	
def metropolis(candidate, current, t):
	return np.exp(-(candidate - current)/t)
	
def step(x,dims,E,t):
	return x + E*np.random.randn(dims)/t
	
def current(lower, upper, dims):
	return lower + np.random.rand(dims) * (upper - lower)

def minimize(objective, x0, temperature, criterion, step, n_iterations, lower, upper,  initialTemperature, dims):
	# T = initialTemperature
	t = initialTemperature
	cur_x = x0
	if not x0:
		cur_x = current(lower,upper, dims)
	cur_obj = objective(cur_x)
	best_x, best_obj = cur_x, cur_obj
	best_i = 0
	for i in range(n_iterations):
		
		candidate_x = step(cur_x, dims, cur_obj,t)
		candidate_x = np.where(candidate_x > upper,upper,candidate_x)
		candidate_x = np.where(candidate_x < lower, lower, candidate_x)
		candidate_obj = objective(candidate_x)
		
		if candidate_obj < best_obj:
			best_obj, best_x, best_i = candidate_obj, candidate_x, i
			# print('>%d f(%s) = %.5f' % (i, best_x, best_obj))
		
		t = temperature(initialTemperature,i)
		crit = criterion(candidate_obj,cur_obj, t)
		
		if candidate_obj < cur_obj or 0.5 <= crit:
			cur_obj, cur_x = candidate_obj, candidate_x
	
	return best_x, best_obj

if __name__ == "__main__":
	import testFunction
	x = []
	obj = []	
	# STEP = 2.5
	# T = 1000
	# DIM = 2
	for i in range(10): 
		a, b = minimize(testFunction.easom, [3,3], temperature, metropolis, step, 50000, -5, 5,  1000, 2)
		print("objective function for iteration %i: %.17f" %(i,b))
		x.append(a)
		obj.append(b)

	best_obj = min(obj)
	best_x = x[obj.index(min(obj))]
	print("Best Objective found: % .17f "%min(obj))
	print("Best Optimal Solution: ", best_x)
