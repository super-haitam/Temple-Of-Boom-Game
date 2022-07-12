from enemyAnimation import EnemyAnimation
from classSprite import Sprite
from settings import *
import pygame
import random


class Enemy(Sprite):
    def __init__(self, spawn_pos: str, pos: tuple):
        direction = "Left" if spawn_pos == "Right" else "Right"
        if spawn_pos == "Top":  # Do random When Top
            direction = random.choice(["Right", "Left"])

        self.animation = EnemyAnimation(direction, "Walk")
        
        self.rect = self.animation.image.get_rect()
        self.spawn(pos)

        self.gravity = 0
        self.speed = 2

        self.last_x = -1
        self.resetJump()

        self.attack = 2
        self.health = 10
        self.is_alive = True

        self.is_player_collision = False
        self.is_enemy_collision = False

    # GRAVITY
    def applyGravity(self):
        self.gravity += .2
        self.rect.y += self.gravity

    # PLAYER INTERACTION
    def attackPlayer(self, player):
        self.animation.changeState("Attack")

        num = int(self.animation.animations["Attack"]["num"] + self.animation.speed)
        if num == self.animation.animations["Attack"]["max"]:
            player.damage(self.attack)

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.is_alive = False

    # COLLISION HANDLING
    def handleEnemyCollision(self, rect):
        # When the Enemy is on top of an other Enemy
        if self.rect.topleft == rect.topleft:
            self.rect.right = rect.left  # OR self.rect.left = rect.right

        # Right Collision
        elif (self.rect.centerx < rect.left <= self.rect.right) and \
                (self.animation.direction == "Right"):
            self.rect.right = rect.left

        # Left Collision
        elif (self.rect.left <= rect.right < self.rect.centerx) and \
                (self.animation.direction == "Left"):
            self.rect.left = rect.right

    def handlePlayerCollision(self, player):
        rect = player.rect
        # Right Collision
        if (self.rect.centerx < rect.left <= self.rect.right) and \
                (self.animation.direction == "Right"):
            self.attackPlayer(player)
            self.rect.right = rect.left

        # Left Collision
        elif (self.rect.left <= rect.right < self.rect.centerx) and \
                (self.animation.direction == "Left"):
            self.attackPlayer(player)
            self.rect.left = rect.right

    def handleGroundCollision(self, rect: pygame.Rect):
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

    def handleJumpPointCollision(self, direction: str, jump_pos: tuple):
        zeros = [0 for _ in range(int(1.6*self.rect.width/self.speed))]
        if self.rect.collidepoint(jump_pos) and \
                    self.animation.direction == direction:
            if random.choice(zeros + [1]):
                self.jump()

    # JUMP
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

    def getBulletHitBy(self, bullets):
        for bullet in bullets:
            if bullet.rect.colliderect(self.rect):
                return bullet

    # MOVEMENT
    def move(self):
        # Jump when Enemy.rect is blocked by something while walking on the ground
        if (self.rect.x == self.last_x) and (self.gravity == 0) and \
                (not self.is_player_collision) and \
                    (not self.is_enemy_collision):  # So that it doesn't jump over game.player
            self.jump()
        self.last_x = self.rect.x
        
        self.applyGravity()
        self.handleJump()

        if self.animation.direction == "Left":
            self.rect.x -= self.speed
        elif self.animation.direction == "Right":
            self.rect.x += self.speed

    # DRAW
    def draw_bar(self, screen):
        bar_rect = pygame.Rect([0, 0, self.health*3, HEIGHT/92])
        bar_rect.bottom = self.rect.top
        bar_rect.centerx = self.rect.centerx

        pygame.draw.rect(screen, GREEN, bar_rect)

    def draw(self, screen):
        self.animation.animate()
        screen.blit(self.animation.image, self.rect.topleft)
        self.draw_bar(screen)
