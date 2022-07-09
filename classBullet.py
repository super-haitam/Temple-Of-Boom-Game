from settings import *
import pygame


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

    def spawn(self, pos: tuple):
        # Spawn only X position
        self.rect.centerx = pos[0]

    def move(self):
        dic = {"Right": 1, "Left": -1}
        self.rect.x += self.speed * dic[self.direction]

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
