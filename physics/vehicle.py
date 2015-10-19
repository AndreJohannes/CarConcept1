import math,numpy

class Vehicle:

	def __init__(self):
		self.position = [0,0]
		self.velocity = [0,0]
		self.angle = 0
		self.angular_velocity = 0

		self.position_suspension_rear = [0,0]
		self.position_suspension_front = [0,0]
		# car geometry, should be stored somewhere else eventually
		# currently the centre of the car is at  98/58; the size of the entire car is (196,116)
		self.center_of_mass = [0, 0] # This is the center of mass with respect to the geometrical centre of the vehicle
		self.position_wheel_rear = [-46,24] # This is the positions with respect to the geometrical centre 
		self.position_wheel_front = [59,24]  # This is the positions with respect to the geometrical centre

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

	def set_angle(angle):
		self.angle = angle

	def get_state_vector():
		return numpy.array([self.position[0], self.position[1], self.velocity[0],self.velocity[1], self.angle, self.angular_velocity, \
			self.position_suspension_front[0], self.position_suspension_front[1],\
			self.position_suspension_rear[0], position_suspension_rear[1] ])

	def get_geometry():
		return self.center_of_mass, self.position_wheel_front, self.position_wheel_rear

	def get_positions(self):
		sin = math.sin(self.angle);
		cos = math.cos(self.angle);
		front_x =  self.center_of_mass[0]+self.position_wheel_front[0]
		front_y =  self.center_of_mass[1]+self.position_wheel_front[1]
		rear_x =  self.center_of_mass[0]+self.position_wheel_rear[0]
		rear_y =  self.center_of_mass[1]+self.position_wheel_rear[1]
		return  self.position, \
			[self.position[0]+cos*front_x+sin*front_y, self.position[1]+cos*front_y-sin*front_x], \
			[self.position[0]+cos*rear_x+sin*rear_y, self.position[1]+cos*rear_y-sin*rear_x]

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



