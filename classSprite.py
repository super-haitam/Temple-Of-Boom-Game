from settings import *
import pygame


class Sprite:
    def spawn(self, pos: tuple):
        self.rect.centerx = pos[0]
        self.rect.bottom = pos[1]
