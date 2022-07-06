import pygame
import os


class PlayerAnimation:
    def __init__(self, direction: str, state: str):
        self.state = state
        self.direction = direction

        image = pygame.image.load(f"./assets/Player/{direction}/{state}/{state}0.png")
        self.image = self.scale(image)

        self.animations = {}
        for animation in ["Stand", "Walk", "Shoot", "Die"]:
            path = "./assets/Player/Left/" + animation
            self.animations[animation] = {}

            # Num of animations
            self.animations[animation]["max"] = len(os.listdir(path)) - 1
            self.animations[animation]["num"] = 0

        self.speed = .25

        self.shoot_count: int
        self.shoot_speed = .1
        self.is_shoot = False

    def scale(self, im):
        return pygame.transform.scale(im, (30, 45))

    def shoot(self):
        self.shoot_count = self.animations["Shoot"]["max"]
        self.is_shoot = True

    def animate(self):
        # This is drawn in the draw() method of Player class
        num = self.animations[self.state]["num"]
        image = pygame.image.load(
            f"./assets/Player/{self.direction}/{self.state}/{self.state}{int(num)}.png")
        self.image = self.scale(image)

        # In case of Shooting
        if self.is_shoot:
            num = self.animations["Shoot"]["max"] - self.shoot_count
            image = pygame.image.load(
                f"./assets/Player/{self.direction}/Shoot/Shoot{int(num)}.png")
            self.image = self.scale(image)

            self.shoot_count -= self.shoot_speed
            if int(self.shoot_count) == 0:
                self.is_shoot = False

        else:
            self.animations[self.state]["num"] += self.speed
            if int(self.animations[self.state]["num"]) == self.animations[self.state]["max"]:
                self.animations[self.state]["num"] = 0
