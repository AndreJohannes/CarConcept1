import math, numpy

# Implementation of a time independend 4th order Runge Kutta solver

class Solver:

	def __init__(self, system):
		self.system = system

	def solve_step(self, step_size, state):
		system = self.system
		# NOTE: s1, s2, s3, s4 are not part of the integration, they merely represent states that get updated every iteration
		k1, s1 = system.get_function(state)
		k2, s2 = system.get_function(numpy.add(state, step_size/2.0*k1))
		k3, s3 = system.get_function(numpy.add(state, step_size/2.0*k2))
		k4, s4 = system.get_function(numpy.add(state, step_size*k3))
		return state + step_size / 6.0 * ( k1+2*k2+2*k3+k4 ), (s1 + 2*s2 +  2*s3 + s4) / 6.0