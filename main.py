from button import Button
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import *
from constants import *
from savedata import save_data, load_data
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
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        dt = clock.tick(60) / 1000
        updatable.update(dt)
        screen.fill((0, 0, 0))

        elapsed_time = pygame.time.get_ticks() - start_time
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
                return "menu", elapsed_time
    return "menu", elapsed_time


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    data = load_data()
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

            best_text = font.render(
                f"best time: {data.get('best_time', 0)}ms", True, (255, 255, 255))
            latest_text = font.render(
                f"last time: {data.get('last_time', 0)}ms", True, (255, 255, 255))
            screen.blit(best_text, (0, 130))
            screen.blit(latest_text, (0, 180))

        elif state == "game":
            result, survival_time = run_game(screen, clock, font)
            data["last_time"] = survival_time
            if survival_time > data.get("best_time", 0):
                data["best_time"] = survival_time
                save_data(data)
            if result == "menu":
                state = "menu"
            elif result == "quit":
                running = False
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
