from settings import *
import pygame


# Class Sprite will be inherited by both Player & Enemy classes and contains the 
#  common functions in both classes
class Sprite:
    def spawn(self, pos: tuple):
        self.rect.centerx = pos[0]
        self.rect.bottom = pos[1]
