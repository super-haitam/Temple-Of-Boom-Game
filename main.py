from pytmx.util_pygame import load_pygame
from classPlayer import Player
from classEnemy import Enemy
from settings import *
import pygame
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

tmx_data = load_pygame("Tiled-Assets/Map.tmx")
ground_tile = tmx_data.get_layer_by_name("Ground")

objects_dict = {}
for obj in tmx_data.objects:
    objects_dict[obj.name] = obj


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player()

        obj = objects_dict["RightSpawn1"]
        self.enemy = Enemy("Right", (obj.x, obj.y))

    def draw(self):
        screen.fill(WHITE)

        for x, y, surf in ground_tile.tiles(): 
            screen.blit(surf, (x*tile_size, y*tile_size))

        self.player.draw(screen)
        self.enemy.draw(screen)
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                    
                    elif event.key == pygame.K_d and not self.player.animation.is_shoot:
                        self.player.shoot()

            # Move the player and enemy
            self.player.handleMovement()
            self.enemy.move()

            for x, y, surf in ground_tile.tiles():
                rect = pygame.Rect([x*tile_size, y*tile_size, tile_size, tile_size])
                
                # Collision with self.player.rect
                if rect.colliderect(self.player.rect):
                    self.player.handleCollision(rect)

                if rect.colliderect(self.enemy.rect):
                    self.enemy.handleCollision(rect)
                
                # Collision with bullet in self.player.Bullets
                for bullet in self.player.bullets:
                    if rect.colliderect(bullet.rect):
                        self.player.removeBullet(bullet)

            self.draw()


game = Game()
game.run()
