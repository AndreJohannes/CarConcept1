import math, numpy

# Implementation of a time independend 4th order Runge Kutta solver

class Solver:

	def __init__(self, step_size, system):
		self.step_size = step_size
		self.system = system

	def solve_step(self, state):
		system = self.system
		k1 = system.get_function(state)
		k2 = system.get_function(numpy.add(state,self.step_size/2.0*k1))
		k3 = system.get_function(numpy.add(state,self.step_size/2.0*k2))
		k4 = system.get_function(numpy.add(state,self.step_size*k3))
		return state + self.step_size/6.0*(k1+2*k2+2*k3+k4)