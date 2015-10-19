import numpy

class Vehicle:

	def __init__(self):
		self.position = [0,0]
		self.velocity = [0,0]
		self.angle = 0
		self.angular_velocity = 0

		self.position_suspension_rear = [0,0]
		self.position_suspension_front = [0,0]
		# car geometry, should be stored somewhere else eventually
		self.center_of_mass = [80, 40]
		self.position_wheel_rear = [25,56]
		self.position_wheel_front = [130,56]		


	def get_state_vector():
		return numpy.array([self.position[0], self.position[1], self.velocity[0],self.velocity[1], self.angle, self.angular_velocity, \
			self.position_suspension_front[0], self.position_suspension_front[1],\
			self.position_suspension_rear[0], position_suspension_rear[1] ])

	def set_state_vector(state):
		self.position[0] = state[0]
		self.position[1] = state[1]
		self.velocity[0] = state[2]
		self.velocity[1] = state[3]
		self.angle = state[4]
		self.angular_velocity = state[5]
		self.position_suspension_front[0] = state[6]
		self.position_suspension_front[1] = state[7]
		self.position_suspension_rear[0] = state[8]
		self.position_suspension_rear[1] = state[9]

	def get_force_and_torque():
		sin = math.sin(rad);
		cos = math.cos(rad);
		force_x = cos*(self.position_suspension_front[0]+self.position_suspension_rear[0])*self.k[0] 
		force_x += sin*(self.position_suspension_front[1]+self.position_suspension_rear[1])*self.k[1] 
		force_y = cos*(self.position_suspension_front[1]+self.position_suspension_rear[1])*self.k[1]
		force_y -= sin*(self.position_suspension_front[0]+self.position_suspension_rear[0])*self.k[0]
		force = [force_x , force_y + mass_vehicle * g_const]

		torque = """ we need the """ * (self.position_suspension_rear[1]-self.position_suspension_front[1] )
		torque = """ 2""" +1
		return force, torque

	def get_function(self, state):
		b=0
		c=0.1*state[3]
		if (state[1]>250):
			b=250-state[1]
			c+=0.5*state[3]
		return numpy.array([state[2], state[3], 0, 5+10*b-c])



