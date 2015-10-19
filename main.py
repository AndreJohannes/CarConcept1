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

state=numpy.array([200,100,0,000])

i=0

while 1:
    for event in pygame.event.get():
         if event.type == pygame.QUIT: sys.exit()

    i=i+0.005

    b=0
    if (state[1]>250):
    	b=250-state[1]
    vehicle, rect = truck.get_vehicle(state[0],state[1],0,b,b)
    state = solver.solve_step(state)
    screen.fill(azur_sky)
    pygame.draw.rect(screen,wine,(0,340,920,200),0)
    screen.blit(vehicle, rect)
    
    #screen.blit(wheel, wheel.get_rect().move(300+50*math.cos(3.14/180*i)),300+50*math.cos(3.14/180*i)))

    pygame.display.flip()
