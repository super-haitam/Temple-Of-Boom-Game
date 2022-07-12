from settings import *
import pygame
import os


class PlayerAnimation:
    def __init__(self, direction: str, state: str):
        self.direction = direction
        self.state = state

        self.animations = {}
        for animation in ["Stand", "Walk", "Shoot", "Die"]:
            path = "./assets/Player/Left/" + animation
            self.animations[animation] = {}

            # Num of animations
            self.animations[animation]["max"] = len(os.listdir(path)) - 1
            self.animations[animation]["num"] = 0

        # Scaled_images Dict to have less run time; Cuz we load & scale each time
        self.scaled_images = {}
        for d in ["Left", "Right"]:
            for s in ["Shoot", "Die", "Stand", "Walk"]:
                for num in range(self.animations[s]["max"]):
                    im = pygame.image.load(f"./assets/Player/{d}/{s}/{s}{num}.png")
                    self.scaled_images[f"{d}/{s}{num}"] = self.scale(im)

        self.image = self.scaled_images[f"{direction}/{state}0"]

        self.speed = .25

        self.shoot_count: int
        self.shoot_speed = .3
        self.is_shoot = False

    def changeState(self, state: str):
        if self.state != state:
            self.animations[self.state]["num"] = 0
            self.state = state

    def scale(self, im):
        return pygame.transform.scale(im, (WIDTH/23, HEIGHT*(9/92)))

    def shoot(self):
        self.shoot_count = self.animations["Shoot"]["max"]
        self.is_shoot = True

    def animate(self):
        # This is drawn in the draw() method of Player class
        num = int(self.animations[self.state]["num"])
        self.image = self.scaled_images[f"{self.direction}/{self.state}{num}"]

        # In case of Shooting
        if self.is_shoot:
            num = self.animations["Shoot"]["max"] - self.shoot_count
            self.image = self.scaled_images[f"{self.direction}/Shoot{int(num)}"]

            self.shoot_count -= self.shoot_speed
            if int(self.shoot_count) == 0:
                self.is_shoot = False

        else:
            self.animations[self.state]["num"] += self.speed
            if int(self.animations[self.state]["num"]) == self.animations[self.state]["max"]:
                self.animations[self.state]["num"] = 0
