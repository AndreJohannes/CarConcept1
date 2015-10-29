import sys, pygame, math, numpy, time, pygame.time
from physics import gameengine

pygame.init()
 
size = width, height = 1280, 720
speed = [0, 0]

step_size = 0.12

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)
engine = gameengine.GameEngine(pygame)
state, displacement = engine.get_initial_state()

start = time.time(); i=0
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT: engine.vehicle.set_throttle(20)
			if event.key == pygame.K_LEFT: engine.vehicle.set_throttle(-5)
			if event.key == pygame.K_r: 
				state, displacement=engine.get_initial_state()
		if event.type == pygame.KEYUP:
            			if event.key == pygame.K_RIGHT: engine.vehicle.set_throttle(0)
            			if event.key == pygame.K_LEFT: engine.vehicle.set_throttle(0)
	
	state, displacement = engine.solve(step_size, state)
    	engine.draw(screen, state, displacement)
    	
    	clock.tick(60)
    	pygame.display.flip()
    	i = i + 1
    	if(time.time()-start > 1):
    		fps = i / (time.time()-start)
    		step_size = 7.2 / fps
    		print "FPS: ", int(fps)
    		start=time.time()
    		i = 0