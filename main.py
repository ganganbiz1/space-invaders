import pygame
import random

# ゲーム設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
ENEMY_DROP = 40
ENEMY_ROWS = 3
ENEMY_COLS = 8

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, direction):
        self.rect.x += ENEMY_SPEED * direction


def create_enemies():
    enemies = pygame.sprite.Group()
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = 80 + col * 80
            y = 50 + row * 60
            enemy = Enemy(x, y)
            enemies.add(enemy)
    return enemies

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = create_enemies()

    enemy_direction = 1
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    player.speed = PLAYER_SPEED
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.speed = 0

        # 敵の移動
        move_down = False
        for enemy in enemies:
            enemy.update(enemy_direction)
            if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.rect.y += ENEMY_DROP

        # 更新
        player_group.update()
        bullets.update()

        # 弾と敵の衝突判定
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)

        # 描画
        screen.fill(BLACK)
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main() 