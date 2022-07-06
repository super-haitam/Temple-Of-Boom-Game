from animation import PlayerAnimation
from classBullet import Bullet
from settings import *
import pygame


class Player:
    def __init__(self):
        # Animate the player
        self.animation = PlayerAnimation("Right", "Stand")

        self.rect = self.animation.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        
        self.gravity = 0
        self.speed = 3

        self.is_jump = False
        self.jump_count = 0

        self.bullets = []

    def removeBullet(self, bullet):
        self.bullets.pop(self.bullets.index(bullet))

    def applyGravity(self):
        self.gravity += .2
        self.rect.y += self.gravity

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.jump_count = 14

    def resetJump(self):
        self.is_jump = False
        self.jump_count = 0

    def handleJump(self):
        if 0 <= self.jump_count:
            self.rect.y -= self.jump_count
            self.jump_count -= 1
        else:
            self.resetJump()

    def handleMovement(self):
        ### Right/Left Movement + Jump + Move Bullets###
        self.applyGravity()
        self.handleJump()

        self.animation.state = "Stand"

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

            self.animation.direction = "Right"
            self.animation.state = "Walk"
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

            self.animation.direction = "Left"
            self.animation.state = "Walk"

        for bullet in self.bullets:
            bullet.move()

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
            self.resetJump()

    def shoot(self):
        self.animation.shoot()

        self.bullets.append(Bullet(self.animation.direction, self.rect))
    
    def draw(self, screen):
        self.animation.animate()
        screen.blit(self.animation.image, self.rect.topleft)

        for bullet in self.bullets:
            bullet.draw(screen)
