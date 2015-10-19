import math

class Truck:

	def __init__(self, pg):
		self.pygame = pg
		self.body = self.pygame.image.load("resources/truck_body.bmp").convert_alpha()
		self.wheel = self.pygame.image.load("resources/wheel.bmp").convert_alpha()
		vehicle_length = self.body.get_width()
		vehicle_height = self.body.get_height() + self.wheel.get_height()-1;
		self.vehicle = self.pygame.Surface([vehicle_length,vehicle_height], self.pygame.SRCALPHA, 32).convert_alpha()

	def get_vehicle(self, pos_x, pos_y, angle,pos_suspension_front, pos_suspension_rear):
		return self._get_surface(pos_suspension_front, pos_suspension_rear, angle),self._get_rect(pos_x, pos_y, angle)

	def _get_surface(self,pos_suspension_front, pos_suspension_rear, angle):
		self.vehicle.fill([0,0,0,0])
		self.vehicle.blit(self.body, self.body.get_rect())
		self.vehicle.blit(self.wheel, self.wheel.get_rect().move(25+pos_suspension_rear[0], 56 + pos_suspension_rear[1]))
		self.vehicle.blit(self.wheel, self.wheel.get_rect().move(130+pos_suspension_front[0], 56 + pos_suspension_front[1]))
		self.vehicle_rotated = self.pygame.transform.rotate(self.vehicle, 180.0/3.14159*angle)
		return  self.vehicle_rotated

	def _get_rect(self, pos_x,pos_y,rad ):
		rect = self.vehicle_rotated.get_rect();
		x = rect.centerx
		y = rect.centery
		rect = rect.move(pos_x-x,pos_y-y).move(-24*0*math.sin(rad),-24*0*math.cos(rad)).move(-59*0*math.cos(rad),59*0*math.sin(rad))
		return rect
