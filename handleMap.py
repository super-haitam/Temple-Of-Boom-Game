from pytmx.util_pygame import load_pygame
from settings import *

class MapHandler:
    def __init__(self, map_num: int):
        self.tmx_data = load_pygame(f"Tiled-Assets/Map{map_num}.tmx")
        self.ground_tile = self.tmx_data.get_layer_by_name("Ground")

        self.objects_dict = {}
        for obj in self.tmx_data.objects:
            self.objects_dict[obj.name] = obj

    def handleGroundCollision(self, sprite):
        # Going off the right side and spawning in the left side
        if WIDTH < sprite.rect.centerx:
            if (self.objects_dict["RightSpawn1-A"].y <= sprite.rect.y) and \
                    (sprite.rect.bottom <= self.objects_dict["RightSpawn1-B"].y):
                obj = self.objects_dict["LeftSpawn1-B"]
                sprite.spawn((obj.x, obj.y))
            elif (self.objects_dict["RightSpawn2-A"].y <= sprite.rect.y) and \
                    (sprite.rect.bottom <= self.objects_dict["RightSpawn2-B"].y):
                obj = self.objects_dict["LeftSpawn2-B"]
                sprite.spawn((obj.x, obj.y))

        # Going off the left side and spawning in the right side
        elif sprite.rect.centerx <= 0:
            if (self.objects_dict["LeftSpawn1-A"].y <= sprite.rect.y) and \
                    (sprite.rect.bottom <= self.objects_dict["LeftSpawn1-B"].y):
                obj = self.objects_dict["RightSpawn1-B"]
                sprite.spawn((obj.x, obj.y))
            elif (self.objects_dict["LeftSpawn2-A"].y <= sprite.rect.y) and \
                    (sprite.rect.bottom <= self.objects_dict["LeftSpawn2-B"].y):
                obj = self.objects_dict["RightSpawn2-B"]
                sprite.spawn((obj.x, obj.y))

    def draw(self, screen):
        for x, y, surf in self.ground_tile.tiles(): 
            screen.blit(surf, (x*tile_size, y*tile_size))
