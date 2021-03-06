from classEnemy import Enemy
import random


class Enemies:
    def __init__(self):
        self.resetLst()

    def resetLst(self):
        self.lst = []

    def addEnemy(self, number: int, objects_dict: dict):
        for i in range(number):
            d = random.choice(["Left", "Right", "Top"])
            obj = objects_dict["TopSpawn"]
            if d in ["Left", "Right"]:
                rand = random.choice([1, 2])
                obj = objects_dict[d + "Spawn" + str(rand) + "-B"]
            enemy = Enemy(d, (obj.x, obj.y))
            self.lst.append(enemy)

    # HANDLE MOVEMENT
    def handleMovement(self, player):
        for enemy in self.lst:
            # Move self.enemies
            enemy.move()

            # Remove any dead enemies
            if not enemy.is_alive:
                self.lst.pop(self.lst.index(enemy))

            if enemy.rect.colliderect(player.rect):
                # Handle Collision with player
                enemy.is_player_collision = True
                enemy.handlePlayerCollision(player)
            else:
                enemy.is_player_collision = False
                enemy.animation.changeState("Walk")

            # Handle Enemy Collision
            self.handleEnemyCollision(enemy)

            # Handle Bullet Collision
            self.handleBulletCollision(enemy, player)

    # COLLISION HANDLING
    def handleEnemyCollision(self, enemy):
        # Handle Collision with other enemies
        enemy.is_enemy_collision = False
        for en in self.lst:
            if (enemy != en) and enemy.rect.colliderect(en.rect) and \
                    (enemy.animation.direction == en.animation.direction):
                enemy.is_enemy_collision = True
                enemy.handleEnemyCollision(en.rect)

    def handleBulletCollision(self, enemy, player):
        # Handle Collision with player.bullets
        hit_bullet = enemy.getBulletHitBy(player.bullets)
        if hit_bullet:
            enemy.damage(player.shoot_attack)
            player.removeBullet(hit_bullet)

    def handleGroundCollision(self, rect):
        for enemy in self.lst:
            if rect.colliderect(enemy.rect):
                enemy.handleGroundCollision(rect)

    def handleJumpPointCollision(self, objects_dict: dict, jump: str):
        if jump.count("LeftJump"):
            for enemy in self.lst:
                jump_pt = objects_dict[jump]
                enemy.handleJumpPointCollision("Left",
                    (jump_pt.x, jump_pt.y-1))
        elif jump.count("RightJump"):
            for enemy in self.lst:
                jump_pt = objects_dict[jump]
                enemy.handleJumpPointCollision("Right",
                    (jump_pt.x, jump_pt.y-1))
    # Draw
    def draw(self, screen):
        for enemy in self.lst:
            enemy.draw(screen)
