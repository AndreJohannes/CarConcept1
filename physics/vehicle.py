import math, numpy
import pdb
from graphics import vehiclegraphics

class Vehicle:

	def __init__(self, pygame, objects):
		self.objects = objects
		self.throttle = 0
		# car geometry, should be stored somewhere else eventually
		# currently the centre of the car is at  98/58; the size of the entire car is (196,116)
		self.center_geometric =[98, 58]
		self.center_of_mass = [10, 20] # This is the center of mass with respect to the geometrical centre of the vehicle
		self.position_wheel_rear = [-46, 24] # This is the positions with respect to the geometrical centre 
		self.position_wheel_front = [59, 24]  # This is the positions with respect to the geometrical centre
		self.CM_to_wheel_front = [self.position_wheel_front[0]-self.center_of_mass[0], self.position_wheel_front[1]-self.center_of_mass[1]] 	
		self.CM_to_wheel_rear = [self.position_wheel_rear[0]-self.center_of_mass[0], self.position_wheel_rear[1]-self.center_of_mass[1]] 
		self.graphics = vehiclegraphics.VehicleGraphics(pygame, self)

	def draw(self, screen, state, displacements):
		suspension_front, suspension_rear = self._get_displacements(state, displacements)
		vehicle_image, vehicle_rect = self.graphics.get_vehicle(400 , state[1], state[7], state[6], state[4], suspension_front, suspension_rear)
		screen.blit(vehicle_image, vehicle_rect)

	def get_geometry(self):
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


	def get_function(self, state, outstate, engine):
		position_x = state[0]; position_y = state[1]
		velocity_x = state[2]; velocity_y = state[3]
		rad = state[4]; angular_velocity = state[5]
		sin = math.sin(rad); cos = math.cos(rad);
		# Next we calculate the position of the centers of the front and rear wheel
		position_wheel_front_x = position_x + cos*self.CM_to_wheel_front[0] + sin*self.CM_to_wheel_front[1]
		position_wheel_front_y = position_y + cos*self.CM_to_wheel_front[1] - sin*self.CM_to_wheel_front[0]
		position_wheel_rear_x = position_x + cos*self.CM_to_wheel_rear[0] + sin*self.CM_to_wheel_rear[1]
		position_wheel_rear_y = position_y + cos*self.CM_to_wheel_rear[1] - sin*self.CM_to_wheel_rear[0]
		
		objects_front = engine.get_collisions(state, position_wheel_front_x, position_wheel_front_y, 26)
		objects_rear = engine.get_collisions(state, position_wheel_rear_x, position_wheel_rear_y, 26)
		
		force_front_x=0; force_front_y=0; touch_front = False; 
		displacement_front_x = 0; displacement_front_y = 0;
		velocity_wheel_front = 3 * (velocity_x + velocity_y) / 1.4;
		for object_front in objects_front:
			ext = object_front[0]; n = object_front[1]; touch_front = True
			force_front_x += 25 * (ext if ext < 0.9 else ext + 10) * n[0] - self.throttle * n[1]
			force_front_y += 25 * (ext if ext < 0.9 else ext + 10) * n[1] + self.throttle * n[0]
			if object_front[2] is not None:
				object_front[2](25 * (ext if ext < 0.9 else ext + 10) * n[0], 25 * (ext if ext < 0.9 else ext + 10) * n[1])
			displacement_front_x, displacement_front_y = self._update_displacement(displacement_front_x, displacement_front_y, n, 26 * ext)
			#displacement_front_x = 26 * ext * n[0] # TODO: this needs to be corrected
			#displacement_front_y = 26 * ext * n[1]
			velocity_wheel_front = 5 * ( -n[1] * velocity_x + n[0] * velocity_y)

		force_rear_x=0; force_rear_y= 0; touch_rear = False;
		displacement_rear_x = 0; displacement_rear_y = 0;
		velocity_wheel_rear = 3*(velocity_x+velocity_y) / 1.4;
		for object_rear in objects_rear:
			ext = object_rear[0]; n = object_rear[1]; touch_rear = True
			force_rear_x += 25 * (ext if ext < 0.9 else ext + 10) * n[0] - self.throttle * n[1] 
			force_rear_y += 25 * (ext if ext < 0.9 else ext + 10) * n[1] + self.throttle * n[0]
			if object_rear[2] is not None:
				object_rear[2](25 * (ext if ext < 0.9 else ext + 10) * n[0], 25 * (ext if ext < 0.9 else ext + 10) * n[1])
			displacement_rear_x, displacement_rear_y = self._update_displacement(displacement_rear_x, displacement_rear_y, n, 26 * ext)
			#displacement_rear_x =  26 * ext * n[0] # TODO: this needs to be corrected
			#displacement_rear_y =  26 * ext * n[1]
			velocity_wheel_rear = 5*(-n[1] * velocity_x + n[0] * velocity_y)

		force_g =  5 # add g-force   ##### TODO:: put all the constants into a seperate file or something like that
		friction =  0.1 + 0.2 * touch_front + 0.2 * touch_rear
		force_x = force_front_x + force_rear_x - friction* velocity_x
		force_y = force_g+force_front_y+force_rear_y - friction * velocity_y 
		torque = force_front_x * (cos * self.CM_to_wheel_front[1] - sin * self.CM_to_wheel_front[0]) + \
			force_front_y * (-cos * self.CM_to_wheel_front[0] - sin * self.CM_to_wheel_front[1]) + \
			force_rear_x * (cos * self.CM_to_wheel_rear[1] - sin * self.CM_to_wheel_rear[0]) + \
			force_rear_y * (-cos * self.CM_to_wheel_rear[0] - sin * self.CM_to_wheel_rear[1])

		outstate[0] = velocity_x
		outstate[1] = velocity_y
		outstate[2] = force_x
		outstate[3] = force_y
		outstate[4] = angular_velocity
		outstate[5] = 0.0003*torque-0.08*angular_velocity
		outstate[6] = velocity_wheel_front
		outstate[7] = velocity_wheel_rear
				
		return numpy.array([displacement_front_x, displacement_front_y, \
				displacement_rear_x, displacement_rear_y])

	def set_throttle(self, throttle):
		self.throttle = throttle;

	def _update_displacement(self, displacement_x, displacement_y, normal, extension):
		current_extension = displacement_x * normal[0] + displacement_y * normal[1];
		if ((extension > 0) and (extension > current_extension)):
			return displacement_x + normal[0] * (extension - current_extension), \
				displacement_y + normal[1] * (extension - current_extension);
		if ((extension < 0) and (extension > current_extension)):
			return displacement_x + normal[0] * (extension - current_extension), \
				displacement_y + normal[1] * (extension - current_extension);
		return displacement_x, displacement_y;

	def _get_displacements(self, state, displacements):
		rad = state[4]; sin = math.sin(rad); cos = math.cos(rad);
		displacement_front_x = cos * displacements[0] - sin * displacements[1]
		displacement_front_y = cos  * displacements[1] + sin * displacements[0]
		displacement_rear_x = cos *displacements[2] - sin * displacements[3]
		displacement_rear_y = cos * displacements[3] + sin * displacements[2]
		return [displacement_front_x, displacement_front_y], [displacement_rear_x, displacement_rear_y]	