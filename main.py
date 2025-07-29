import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from constants import *
from player import *
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	running = True
	clock = pygame.time.Clock()
	dt = 0

	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()

	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
 
	Player.containers = updatable, drawable
	player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
 
	Shot.containers = updatable, drawable, shots

	Asteroid.containers = updatable, drawable, asteroids
	AsteroidField.containers = updatable
	asteroidfield = AsteroidField()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		dt = clock.tick(60)/1000
		updatable.update(dt)
  
		screen.fill((0, 0, 0))
		for drawable_obj in drawable:
			drawable_obj.draw(screen)
		pygame.display.flip()

		for asteroid in asteroids:
			if asteroid.collision(player):
				print("Game over!")
				running = False
	pygame.quit()
if __name__ == "__main__":
	main()
