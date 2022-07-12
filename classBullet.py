from settings import *
import pygame
import time


class Bullet:
    def __init__(self, direction: str, player_rect: pygame.Rect):
        self.direction = direction
        self.rect = pygame.Rect([0, 0, WIDTH/86, HEIGHT/78])

        if self.direction == "Right":
            self.rect.centerx = player_rect.right
        elif self.direction == "Left":
            self.rect.centerx = player_rect.left
        self.rect.centery = player_rect.centery

        self.speed = 4

        self.fire_time = time.time()
        self.lifetime = 4

    def getTimeUp(self):
        return self.lifetime < (time.time() - self.fire_time)

    def spawn(self, pos: tuple):
        # Spawn only X position
        self.rect.centerx = pos[0]

    def move(self):
        dic = {"Right": 1, "Left": -1}
        self.rect.x += self.speed * dic[self.direction]

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
