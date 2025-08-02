from button import Button
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import *
from constants import *
import pygame
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

def run_game(screen, clock, font):
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = updatable, drawable
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = updatable, drawable, shots
    Asteroid.containers = updatable, drawable, asteroids
    AsteroidField.containers = updatable
    asteroidfield = AsteroidField()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        dt = clock.tick(60) / 1000
        updatable.update(dt)
        screen.fill((0, 0, 0))

        elapsed_time = pygame.time.get_ticks()
        timer_surface = font.render(
            f"Time: {elapsed_time}ms", True, (255, 255, 255))
        x = SCREEN_WIDTH - timer_surface.get_width() - 10
        screen.blit(timer_surface, (x, 10))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
                    break
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                pygame.time.delay(2000)
                return "menu"


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    state = "menu"

    def start_game():
        nonlocal state
        state = "game"

    def quit_game():
        nonlocal running
        running = False

    buttons = [
		Button("start", 0, 0, 200, 50, start_game, font),
		Button("quit", 0, 60, 200, 50, quit_game, font)
	]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "menu":
                for button in buttons:
                    button.handle_event(event)
        screen.fill((0, 0, 0))

        if state == "menu":
            for button in buttons:
                button.draw(screen)
        elif state == "game":
            result = run_game(screen, clock, font)
            if result == "menu":
                state = "menu"
            elif result == "quit":
                running = False
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
	main()
