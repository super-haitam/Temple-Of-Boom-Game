from settings import *
import pygame
import os


class EnemyAnimation:
    def __init__(self, direction: str, state: str):
        self.direction = direction
        self.state = state

        image = pygame.image.load(f"./assets/Enemy/{direction}/{state}/{state}0.png")
        self.image = self.scale(image)

        self.animations = {}
        for animation in ["Stand", "Walk", "Attack", "Hurt", "Die"]:
            path = "./assets/Enemy/Left/" + animation
            self.animations[animation] = {}

            # Num of animations
            self.animations[animation]["max"] = len(os.listdir(path)) - 1
            self.animations[animation]["num"] = 0

        self.attack_speed = .2
        self.speed = .25

    def changeState(self, state: str):
        if self.state != state:
            self.animations[self.state]["num"] = 0
            self.state = state

    def scale(self, image):
        return pygame.transform.scale(image, (WIDTH/30, HEIGHT*(3/37)))

    def animate(self):
        num = int(self.animations[self.state]["num"])
        image = pygame.image.load(
            f"./assets/Enemy/{self.direction}/{self.state}/{self.state}{num}.png")
        self.image = self.scale(image)

        if self.state == "Attack":
            self.animations["Attack"]["num"] += self.attack_speed
        else:
            self.animations[self.state]["num"] += self.speed

        if int(self.animations[self.state]["num"]) == self.animations[self.state]["max"]:
            self.animations[self.state]["num"] = 0
