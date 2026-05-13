import pygame
import sys
from abc import ABC, abstractmethod
import random

class Game(ABC):
    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class SnakeGame(Game):
    SPEED = 20

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.snake = [(100, 100)]
        self.direction = (1, 0)
        self.food = (200, 200)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction[1] == 0:
            self.direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.direction[1] == 0:
            self.direction = (0, 1)
        elif keys[pygame.K_LEFT] and self.direction[0] == 0:
            self.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.direction[0] == 0:
            self.direction = (1, 0)

    def update(self):
        head_x, head_y = self.snake[0]

        dx, dy = self.direction

        new_head_x = head_x + dx * self.SPEED
        new_head_y = head_y + dy * self.SPEED

        if new_head_x < 0:
            new_head_x = self.screen_size[0]
        if new_head_x > self.screen_size[0]:
            new_head_x = 0

        if new_head_y < 0:
            new_head_y = self.screen_size[1]
        if new_head_y > self.screen_size[1]:
            new_head_y = 0

        new_head = (new_head_x, new_head_y)
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = (random.randrange(0, 600, 20), random.randrange(0, 400, 20))
        else:
            self.snake.pop()

    def draw(self, screen):
        for segment in self.snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, 20, 20))
        pygame.draw.rect(screen, (255, 0, 0), (*self.food, 20, 20))


class DodgerGame(Game):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.player_size = (30, 30)
        self.enemy_size = (40, 40)
        self.player = pygame.Rect(
            (self.screen_size[0] - self.player_size[0]) / 2,
            self.screen_size[1] - self.player_size[1],
            *self.player_size
        )
        self.enemies = [pygame.Rect(random.randint(0, self.screen_size[0] - self.enemy_size[0]), 0, *self.enemy_size) for _ in range(3)]

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= 10
            self.player.x = max(self.player.x, 0)
        if keys[pygame.K_RIGHT]:
            self.player.x += 10
            self.player.x = min(self.player.x, self.screen_size[0] - self.player_size[0])

    def update(self):
        for enemy in self.enemies:
            enemy.y += 5
            if enemy.y > self.screen_size[1]:
                enemy.y = 0
                enemy.x = random.randint(0, self.screen_size[0] - self.enemy_size[0])

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.player)
        for enemy in self.enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)


class GameEngine(ABC):
    def __init__(self):
        pygame.init()
        screen_size = (600, 400)
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.game = self.create_game(screen_size)

    @abstractmethod
    def create_game(self, screen_size) -> Game | None:
        return None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((30, 30, 30))
            
            if self.game is not None:
                self.game.handle_events()
                self.game.update()
                self.game.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(10)


class SnakeEngine(GameEngine):
    def create_game(self, screen_size):
        return SnakeGame(screen_size)


class DodgerEngine(GameEngine):
    def create_game(self, screen_size):
        return DodgerGame(screen_size)


if __name__ == "__main__":
    engine = SnakeEngine()
    # engine = DodgerEngine()

    engine.run()
