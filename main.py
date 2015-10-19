import sys, pygame,math,numpy
from graphics import truck
from physics import  runge_kutta_solver
from physics import vehicle 

pygame.init()
 
size = width, height = 920, 540
speed = [0, 0]
azur_sky = 181, 226, 244
wine = 114, 47, 55
black = 0,0,0
transparent = 0,0,0,0

screen = pygame.display.set_mode(size)
wheel = pygame.image.load("resources/wheel.png").convert_alpha()
truck = truck.Truck(pygame)
solver = runge_kutta_solver.Solver(0.03, vehicle.Vehicle())

state=numpy.array([200,200,0,0,0.01,0])

i=0

while 1:
	for event in pygame.event.get():
    		if event.type == pygame.QUIT: sys.exit()
    		if event.type == pygame.KEYDOWN:
        			if event.key == pygame.K_LEFT:
            				i -= 0.01

        			if event.key == pygame.K_RIGHT:
            				i += 0.01

	suspension_front, suspension_rear = solver.system.get_suspensions(state)    	
	vehicle, rect = truck.get_vehicle(state[0],state[1],state[4],suspension_front, suspension_rear)
    	state = solver.solve_step(state)
    	screen.fill(azur_sky)
    	pygame.draw.rect(screen,wine,(0,340,920,200),0)
    	screen.blit(vehicle, rect)

    	pygame.display.flip()
