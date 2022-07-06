from pytmx.util_pygame import load_pygame
from settings import *
from classPlayer import Player
import pygame
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

tmx_data = load_pygame("Tiled-Assets/Map.tmx")
ground_tile = tmx_data.get_layer_by_name("Ground")


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player()

    def draw(self):
        screen.fill(WHITE)

        for x, y, surf in ground_tile.tiles(): 
            screen.blit(surf, (x*tile_size, y*tile_size))

        self.player.draw(screen)
        
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

            self.player.handleMovement()

            for x, y, surf in ground_tile.tiles():
                rect = pygame.Rect([x*tile_size, y*tile_size, tile_size, tile_size])
                if rect.colliderect(self.player.rect):
                    self.player.handleCollision(rect)

            self.draw()


game = Game()
game.run()
