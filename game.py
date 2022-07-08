from pytmx.util_pygame import load_pygame
from classPlayer import Player
from classEnemy import Enemy
from settings import *
import random
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

        self.enemies = []
        for i in range(3):
            d = random.choice(["Left", "Right", "Top"])
            obj = objects_dict["TopSpawn"]
            if d in ["Left", "Right"]:
                rand = random.choice([1, 2])
                obj = objects_dict[d + "Spawn" + str(rand) + "-B"]
            enemy = Enemy(d, (obj.x, obj.y))
            self.enemies.append(enemy)

    def draw(self):
        screen.fill(WHITE)

        for x, y, surf in ground_tile.tiles(): 
            screen.blit(surf, (x*tile_size, y*tile_size))

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)
        
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

            # Move self.enemies and Handle Collision with self.player.bullets
            for enemy in self.enemies:
                enemy.move()

                hit_bullet = enemy.getBulletHitBy(self.player.bullets)
                if hit_bullet:
                    enemy.damage(self.player.shoot_attack)
                    self.player.removeBullet(hit_bullet)

                    # Remove any dead enemies
                    if not enemy.is_alive:
                        self.enemies.pop(self.enemies.index(enemy))

            # Handle Collisions with Ground
            for x, y, surf in ground_tile.tiles():
                rect = pygame.Rect([x*tile_size, y*tile_size, tile_size, tile_size])
                
                # Collision with self.player.rect
                if rect.colliderect(self.player.rect):
                    self.player.handleCollision(rect)

                # Collision with enemies.rect
                for enemy in self.enemies:
                    if rect.colliderect(enemy.rect):
                        enemy.handleCollision(rect)
                
                # Collision with bullet in self.player.Bullets
                for bullet in self.player.bullets:
                    if rect.colliderect(bullet.rect):
                        self.player.removeBullet(bullet)

            # Teleportation 
            sprites = [self.player] + self.enemies + self.player.bullets
            for sprite in sprites:
                # Going off the right side and spawning in the left side
                if WIDTH < sprite.rect.centerx:
                    if (objects_dict["RightSpawn1-A"].y <= sprite.rect.y) and \
                            (sprite.rect.bottom <= objects_dict["RightSpawn1-B"].y):
                        obj = objects_dict["LeftSpawn1-B"]
                        sprite.spawn((obj.x, obj.y))
                    elif (objects_dict["RightSpawn2-A"].y <= sprite.rect.y) and \
                            (sprite.rect.bottom <= objects_dict["RightSpawn2-B"].y):
                        obj = objects_dict["LeftSpawn2-B"]
                        sprite.spawn((obj.x, obj.y))

                # Going off the left side and spawning in the right side
                elif sprite.rect.centerx <= 0:
                    if (objects_dict["LeftSpawn1-A"].y <= sprite.rect.y) and \
                            (sprite.rect.bottom <= objects_dict["LeftSpawn1-B"].y):
                        obj = objects_dict["RightSpawn1-B"]
                        sprite.spawn((obj.x, obj.y))
                    elif (objects_dict["LeftSpawn2-A"].y <= sprite.rect.y) and \
                            (sprite.rect.bottom <= objects_dict["LeftSpawn2-B"].y):
                        obj = objects_dict["RightSpawn2-B"]
                        sprite.spawn((obj.x, obj.y))

            self.draw()
