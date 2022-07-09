from playerAnimation import PlayerAnimation
from classSprite import Sprite
from classBullet import Bullet
from settings import *
import pygame


class Player(Sprite):
    def __init__(self):
        # Animate the player
        self.animation = PlayerAnimation("Right", "Stand")

        self.rect = self.animation.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        
        self.gravity = 0
        self.speed = 3

        self.resetJump()

        self.bullets = []

        self.health = 30
        self.shoot_attack = 3

    def damage(self, amount):
        self.health -= amount

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
        ### Right/Left Movement + Jump + Move Bullets ###
        self.handleJump()
        self.applyGravity()

        # Not allow going off screen by Top
        if self.rect.y < 0:
            self.resetJump()

        self.animation.state = "Stand"

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

            self.animation.direction = "Right"
            self.animation.changeState("Walk")
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

            self.animation.direction = "Left"
            self.animation.changeState("Walk")

        # Move Bullets and Destroy them when Out Of Bounds
        for bullet in self.bullets:
            bullet.move()
            if (bullet.rect.right <= 0) or (WIDTH <= bullet.rect.left):
                self.removeBullet(bullet)

    def handleGroundCollision(self, rect):
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
    
    def draw_bar(self, screen):
        bar_rect = pygame.Rect([0, 0, self.health, HEIGHT/92])
        bar_rect.bottom = self.rect.top
        bar_rect.centerx = self.rect.centerx

        pygame.draw.rect(screen, GREEN, bar_rect)

    def draw(self, screen):
        self.animation.animate()
        screen.blit(self.animation.image, self.rect.topleft)
        self.draw_bar(screen)

        for bullet in self.bullets:
            bullet.draw(screen)
