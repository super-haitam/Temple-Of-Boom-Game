from handleMap import MapHandler
from classEnemies import Enemies
from classPlayer import Player
from classEnemy import Enemy
from settings import *
import pygame
pygame.init()


# Screen
pygame.display.set_caption("Platformer-Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Tmx map
map_handler = MapHandler(2)


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player()

        self.enemies = Enemies()
        self.enemies.addEnemy(3, map_handler.objects_dict)

    def draw(self):
        screen.fill(BLACK)

        # Draw Ground
        map_handler.draw(screen)

        # Draw Player
        self.player.draw(screen)

        # Draw Enemies
        self.enemies.draw(screen)
        
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

            # Move the player
            self.player.handleMovement()

            # Handle Movement of enemies
            self.enemies.handleMovement(self.player)

            # Handle Collisions with Ground
            for x, y, surf in map_handler.ground_tile.tiles():
                rect = pygame.Rect([x*tile_size, y*tile_size, tile_size, tile_size])
                
                # Collision with self.player.rect
                if rect.colliderect(self.player.rect):
                    self.player.handleGroundCollision(rect)

                # Collision with enemies.rect
                self.enemies.handleGroundCollision(rect)
                
                # Collision with bullet in self.player.Bullets
                for bullet in self.player.bullets:
                    if rect.colliderect(bullet.rect):
                        self.player.removeBullet(bullet)

            # Teleportation
            sprites = [self.player] + self.enemies.lst + self.player.bullets
            for sprite in sprites:
                map_handler.handleTeleport(sprite)

            for jump in map_handler.objects_dict:
                if jump.count("LeftJump"):
                    for enemy in self.enemies.lst:
                        jump_pt = map_handler.objects_dict[jump]
                        enemy.handleJumpPointCollision("Left",
                            (jump_pt.x, jump_pt.y-1))
                elif jump.count("RightJump"):
                    for enemy in self.enemies.lst:
                        jump_pt = map_handler.objects_dict[jump]
                        enemy.handleJumpPointCollision("Right",
                            (jump_pt.x, jump_pt.y-1))

            self.draw()
