import sys, pygame, math, numpy, time
from graphics import truck
from physics import  runge_kutta_solver
from physics import vehicle 
from physics import objects

pygame.init()
 
size = width, height = 920, 540
speed = [0, 0]
azur_sky = 181, 226, 244
wine = 114, 47, 55
black = 0, 0, 0
transparent = 0, 0, 0, 0

screen = pygame.display.set_mode(size)
#wheel = pygame.image.load("resources/wheel.png").convert_alpha()
objects = objects.Objects()
vehicle = vehicle.Vehicle(objects)
truck = truck.Truck(pygame, vehicle)
solver = runge_kutta_solver.Solver(0.03, vehicle)

state=numpy.array([200, 340, 0, 0, 0, 0,0 ,0])
displacements = numpy.array([0, 0, 0, 0])


start = time.time(); i=0
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:solver.system.set_throttle(10)
			if event.key == pygame.K_LEFT:solver.system.set_throttle(-5)
			if event.key == pygame.K_r: 
				state=numpy.array([200, 340, 0, 0, 0, 0, 0 ,0]); displacements = numpy.array([0, 0, 0, 0])
		if event.type == pygame.KEYUP:
            			if event.key == pygame.K_RIGHT:solver.system.set_throttle(0)
            			if event.key == pygame.K_LEFT:solver.system.set_throttle(0)
    	
    	
    	state[0] = state[0] % 1000
	suspension_front, suspension_rear = solver.system.get_displacements(state, displacements)
	vehicle_image, vehicle_rect = truck.get_vehicle(state[0] , state[1], state[7], state[6], state[4], suspension_front, suspension_rear)
    	state, displacements = solver.solve_step(state)
    	screen.fill(azur_sky)
    	bars = objects.get_bars()
    	for bar in bars:
    		pygame.draw.line(screen, wine, bar.A, bar.B, 5)
    	#pygame.draw.rect(screen,wine,(0,340,920,200),0)
    	screen.blit(vehicle_image, vehicle_rect)

    	pygame.display.flip()

    	i = i + 1
    	if(time.time()-start > 1):
    		print i, time.time()-start
    		start=time.time()
    		i = 0