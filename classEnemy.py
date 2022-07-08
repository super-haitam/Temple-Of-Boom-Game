from enemyAnimation import EnemyAnimation
from classSprite import Sprite
from settings import *
import pygame
import random


class Enemy(Sprite):
    def __init__(self, spawn_pos: str, pos: tuple):
        self.direction = "Left" if spawn_pos == "Right" else "Right"
        if spawn_pos == "Top":  # Do random When Top
            self.direction = random.choice(["Right", "Left"])

        self.animation = EnemyAnimation(self.direction, "Walk")
        
        self.rect = self.animation.image.get_rect()

        self.spawn(pos)

        self.gravity = 0
        self.speed = 2

        self.last_x = -1
        self.resetJump()

        self.is_alive = True
        self.health = self.max_health = 10

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

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.jump_count = 12

    def resetJump(self):
        self.is_jump = False
        self.jump_count = 0

    def handleJump(self):
        if 0 <= self.jump_count:
            self.rect.y -= self.jump_count
            self.jump_count -= 1
        else:
            self.resetJump()

    def getBulletHitBy(self, bullets):
        for bullet in bullets:
            if bullet.rect.colliderect(self.rect):
                return bullet

    def move(self):
        # Jump when Enemy.rect is blocked by something while walking on the ground
        if (self.rect.x == self.last_x) and self.gravity == 0:
            self.jump()
        self.last_x = self.rect.x
        
        self.applyGravity()
        self.handleJump()

        if self.direction == "Left":
            self.rect.x -= self.speed
        elif self.direction == "Right":
            self.rect.x += self.speed

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.is_alive = False

    def draw_bar(self, screen):
        bar_rect = pygame.Rect([0, 0, self.health*3, HEIGHT/92])
        bar_rect.bottom = self.rect.top
        bar_rect.centerx = self.rect.centerx

        pygame.draw.rect(screen, GREEN, bar_rect)

    def draw(self, screen):
        self.animation.animate()
        screen.blit(self.animation.image, self.rect.topleft)
        self.draw_bar(screen)
