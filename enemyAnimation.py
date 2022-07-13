from settings import *
import pygame
import os


class EnemyAnimation:
    def __init__(self, direction: str, state: str):
        self.direction = direction
        self.state = state
        self.is_alive = True
        self.is_dying = False

        self.animations = {}
        for animation in ["Stand", "Walk", "Attack", "Hurt", "Die"]:
            path = "./assets/Enemy/Left/" + animation
            self.animations[animation] = {}

            # Num of animations
            self.animations[animation]["max"] = len(os.listdir(path)) - 1
            self.animations[animation]["num"] = 0

        # Scaled_images Dict to have less run time; Cuz we used to load & scale each time
        self.scaled_images = {}
        for d in ["Left", "Right"]:
            for s in ["Attack", "Die", "Hurt", "Stand", "Walk"]:
                for num in range(self.animations[s]["max"]):
                    im = pygame.image.load(f"./assets/Enemy/{d}/{s}/{s}{num}.png")
                    self.scaled_images[f"{d}/{s}{num}"] = self.scale(im)

        self.image = self.scaled_images[f"{direction}/{state}0"]

        self.attack_speed = .2
        self.speed = .25

    def changeState(self, state: str):
        if self.state != state:
            self.animations[self.state]["num"] = 0
            self.state = state

    def scale(self, image):
        return pygame.transform.scale(image, (WIDTH/30, HEIGHT*(3/37)))

    def animate(self):
        if self.is_dying:
            num = int(self.animations["Die"]["num"])
            self.image = self.scaled_images[f"{self.direction}/Die{num}"]

            self.animations["Die"]["num"] += self.speed
            if int(self.animations["Die"]["num"]) == self.animations["Die"]["max"]:
                self.is_alive = False
                self.animations["Die"]["num"] = 0
            
        else:
            num = int(self.animations[self.state]["num"])
            self.image = self.scaled_images[f"{self.direction}/{self.state}{num}"]

            if self.state == "Attack":
                self.animations["Attack"]["num"] += self.attack_speed
            else:
                self.animations[self.state]["num"] += self.speed

            if int(self.animations[self.state]["num"]) == self.animations[self.state]["max"]:
                self.animations[self.state]["num"] = 0
