import math

class Truck:

	def __init__(self, pg, vehicle_data):
		self.pygame = pg
		self.body = self.pygame.image.load("resources/truck_body.bmp").convert_alpha()
		self.wheel = self.pygame.image.load("resources/wheel.bmp").convert_alpha()
		vehicle_length = self.body.get_width()
		vehicle_height = self.body.get_height() + self.wheel.get_height()-1;
		self.vehicle = self.pygame.Surface([vehicle_length,vehicle_height], self.pygame.SRCALPHA, 32).convert_alpha()
		self.vehicle_data = vehicle_data

	def get_vehicle(self, pos_x, pos_y, angle_wheel_front, angle_wheel_rear, angle,pos_suspension_front, pos_suspension_rear):
		return self._get_surface(pos_suspension_front, pos_suspension_rear, \
			angle ,angle_wheel_front, angle_wheel_rear),self._get_rect(pos_x, pos_y, angle)

	def _get_surface(self,pos_suspension_front, pos_suspension_rear, angle ,angle_wheel_front, angle_wheel_rear):
		self.vehicle.fill([0, 0, 0, 0])
		self.vehicle.blit(self.body, self.body.get_rect())
		wheel_rotated = self.pygame.transform.rotate(self.wheel, -angle_wheel_front)
		center_x = wheel_rotated.get_rect().centerx
		center_y = wheel_rotated.get_rect().centery
		offset1 = self.vehicle_data.center_geometric[0] + self.vehicle_data.position_wheel_rear[0] -1
		offset2 = self.vehicle_data.center_geometric[1] + self.vehicle_data.position_wheel_rear[1] -1
		self.vehicle.blit(wheel_rotated, wheel_rotated.get_rect().\
			move(offset1 + pos_suspension_rear[0] -center_x, offset2+ pos_suspension_rear[1]-center_y))
		wheel_rotated = self.pygame.transform.rotate(self.wheel, -angle_wheel_rear)
		center_x = wheel_rotated.get_rect().centerx
		center_y = wheel_rotated.get_rect().centery
		offset1 = self.vehicle_data.center_geometric[0] + self.vehicle_data.position_wheel_front[0] -1
		offset2 = self.vehicle_data.center_geometric[1] + self.vehicle_data.position_wheel_front[1] -1
		self.vehicle.blit(wheel_rotated, wheel_rotated.get_rect().\
			move(offset1 + pos_suspension_front[0]-center_x, offset2 + pos_suspension_front[1]-center_y))
		self.vehicle_rotated = self.pygame.transform.rotate(self.vehicle, 180.0 / 3.14159 * angle)
		return  self.vehicle_rotated

	def _get_rect(self, pos_x,pos_y,rad ):
		rect = self.vehicle_rotated.get_rect();
		x = rect.centerx
		y = rect.centery
		offset1 = self.vehicle_data.center_of_mass[1]
		offset2 = self.vehicle_data.center_of_mass[0]
		rect = rect.move(pos_x-x,pos_y-y).move(-offset1*math.sin(rad), \
			-offset1*math.cos(rad)).move(-offset2*math.cos(rad), offset2*math.sin(rad))
		return rect
