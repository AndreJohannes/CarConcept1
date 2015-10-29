import numpy, math
from collections import namedtuple

# class that holds a list of all objects in the world and calculates the collision

class Objects:

	# Class that represents the objects of bars, ie. plane grounds
	class Bar(object):

		def __init__(self, A, B):
			self.A = A # A and B are the end points of the bar
			self.B = B
			AB = B - A
			self.tangent = AB / numpy.linalg.norm(AB)
			rot = numpy.array([[0,1],[-1,0]])
			self.n = numpy.dot(rot, (AB) / numpy.linalg.norm(AB)); n = self.n # vector perpendicular to the bar
			self.denominator =  (AB[1]*n[0]-AB[0]*n[1])

	# Class that represents the object of point, i.e a corner. 	
	class Point(object):

		def __init__(self, A):
			self.A = A

	
	def __init__(self, pygame):
		bar_list = []
		point_list = []
		self.bar_list = bar_list
		self.pygame = pygame 
		# TODO: the world objects maybe should be loaded from tha xml file
		bar_list.append( Objects.Bar(numpy.array([-500,430]),numpy.array([1200, 430])) )
		bar_list.append( Objects.Bar(numpy.array([1200, 430]), numpy.array([1300,385])) )
		bar_list.append( Objects.Bar(numpy.array([2500, 185]), numpy.array([2600,130])) )
		bar_list.append( Objects.Bar(numpy.array([2600, 130]), numpy.array([3500,130])) )
		
		self.point_list = point_list

	def draw(self, screen, offset_x):
		wine = 114, 47, 55
		pygame = self.pygame
		bars = self.bar_list;
    		for bar in bars:
    			pygame.draw.line(screen, wine, bar.A - numpy.array([-400+offset_x,0]), bar.B - numpy.array([-400+offset_x,0]), 5)


	def get_objects(self, Cx, Cy, distance_threshold):
		object_list = []
		for bar  in self.bar_list:
			x, y, n = self._get_bar(bar, Cx, Cy, distance_threshold)
			if x is not None:
				object_list.append([y, n, None]) 		

		if(not object_list):
			for point in self.point_list:
				x, n = self._get_point(point, Cx, Cy, distance_threshold)
				if x is not None:
					object_list.append([x, n, None])

		return object_list

	def _get_bar(self, bar, Cx, Cy, distance_threshold):
		A = bar.A; n = bar.n
		AC = [Cx - A[0], Cy - A[1]]
		numerator = AC[1] * n[0] - AC[0] * n[1]
		x = numerator / bar.denominator
		if (x<0 or x>1): 
			return  None, None, None
		AB = bar.A-bar.B	
		numerator = AC[1] *AB[0] - AC[0] * AB[1] 
		y = numerator / bar.denominator
		if (y<0 or y> distance_threshold): 
			return  None, None, None
		y = (distance_threshold- y) / distance_threshold
		return  x, y, bar.n

	def _get_point(self, point, Cx, Cy, distance_threshold):
		A = point.A
		dist_sqr = (Cx-A[0])*(Cx-A[0]) + (Cy-A[1])*(Cy-A[1])
		if (dist_sqr > distance_threshold * distance_threshold): 
			return None, None
		n = numpy.array([Cx-A[0],Cy-A[1]]); n = n / numpy.linalg.norm(n)
		return  (distance_threshold - math.sqrt(dist_sqr)) / distance_threshold, n
