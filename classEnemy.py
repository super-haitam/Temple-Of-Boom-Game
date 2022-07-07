from enemyAnimation import EnemyAnimation
from settings import *
import pygame


class Enemy:
    def __init__(self, spawn_pos: str, pos: tuple):
        direction = "Left" if spawn_pos == "Right" else "Right"
        self.animation = EnemyAnimation(direction, "Walk")
        
        self.rect = self.animation.image.get_rect()

        self.spawn(spawn_pos, pos)

        self.gravity = 0
        self.speed = 2

    def applyGravity(self):
        self.gravity += .2
        self.rect.y += self.gravity

    def handleCollision(self, rect):
        # When the ground stops you from Fall Death 
        if self.rect.centery < rect.top <= self.rect.bottom:
            self.rect.bottom = rect.top
            self.gravity = 0
        
        # When walls stop you
        elif self.rect.centerx < rect.left <= self.rect.right:
            self.rect.right = rect.left
        elif self.rect.left <= rect.right < self.rect.centerx:
            self.rect.left = rect.right

        # When you crash on the ceiling
        elif self.rect.top <= rect.bottom < self.rect.centery:
            self.rect.top = rect.bottom

    def move(self):
        self.applyGravity()
        self.rect.x -= self.speed

    def spawn(self, spawn_pos: str, pos: tuple):
        if spawn_pos == "Left":
            # For Spawning in LeftSpawn
            self.rect.topright = pos
        elif spawn_pos == "Right":
            # For Spawning in RightSpawn
            self.rect.topleft = pos
        elif spawn_pos == "Top":
            # For Spawning in TopSpawn
            self.rect.centerx = pos[0]
            self.rect.bottom = pos[1]

    def draw(self, screen):
        self.animation.animate()
        screen.blit(self.animation.image, self.rect.topleft)
