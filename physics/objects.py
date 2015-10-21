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

	# Class that represents the object of  point, i.e a corner. 	
	class Point(object):

		def __init__(self, A):
			self.A = A

	
	def __init__(self):
		bar_list = []
		point_list = []
		self.bar_list = bar_list
		# TODO: the world objects maybe should be loaded from tha xml file
		bar_list.append( Objects.Bar(numpy.array([-500,430]),numpy.array([1500, 430])) )
		bar_list.append( Objects.Bar(numpy.array([200,430]),numpy.array([600, 290])) )
		bar_list.append( Objects.Bar(numpy.array([600, 290]), numpy.array([800,430])) )
		point_list.append( Objects.Point(numpy.array([600,290])))
		self.point_list = point_list

	def get_objects(self, Cx, Cy):
		object_list = []
		for bar  in self.bar_list:
			x, y, n = self._get_bar(bar, Cx, Cy)
			if x is not None:
				object_list.append([y, n]) 		

		if(not object_list):
			for point in self.point_list:
				x, n = self._get_point(point, Cx, Cy)
				if x is not None:
					object_list.append([x, n])

		return object_list

	def get_bars(self):
		return self.bar_list

	def _get_bar(self, bar, Cx, Cy):
		A = bar.A; n = bar.n
		AC = [Cx - A[0], Cy - A[1]]
		numerator = AC[1] * n[0] - AC[0] * n[1]
		x = numerator / bar.denominator
		if (x<0 or x>1): 
			return  None, None, None
		AB = bar.A-bar.B	
		numerator = AC[1] *AB[0] - AC[0] * AB[1] 
		y = numerator / bar.denominator
		if (y<0 or y> 26): # TODO: define the 26 globally
			return  None, None, None
		y = (26 - y) / 26
		return  x, y, bar.n

	def _get_point(self, point, Cx, Cy):
		A = point.A
		dist_sqr = (Cx-A[0])*(Cx-A[0]) + (Cy-A[1])*(Cy-A[1])
		if (dist_sqr > 26*26): # define the 26 globally
			return None, None
		n = numpy.array([Cx-A[0],Cy-A[1]]); n = n / numpy.linalg.norm(n)
		return  (26-math.sqrt(dist_sqr))/26, n
