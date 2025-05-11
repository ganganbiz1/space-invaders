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
BLACK = (10, 10, 30)
GREEN = (80, 255, 120)
RED = (255, 80, 80)
YELLOW = (255, 255, 80)
BLUE = (80, 180, 255)
PINK = (255, 120, 255)
ORANGE = (255, 180, 80)

ENEMY_COLORS = [RED, YELLOW, BLUE, PINK, ORANGE]

FONT_NAME = "arial"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.create_sprite()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        self.speed = 0

    def create_sprite(self):
        surf = pygame.Surface((50, 30), pygame.SRCALPHA)
        # ドット絵風シップ
        pygame.draw.rect(surf, GREEN, (10, 20, 30, 8))
        pygame.draw.rect(surf, GREEN, (20, 10, 10, 20))
        pygame.draw.rect(surf, WHITE, (24, 5, 2, 5))
        pygame.draw.rect(surf, (0, 0, 0, 80), (0, 0, 50, 30), 2)
        return surf

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.image, YELLOW, (0, 0, 5, 15), border_radius=2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = self.create_sprite(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def create_sprite(self, color):
        surf = pygame.Surface((40, 30), pygame.SRCALPHA)
        # ドット絵風インベーダー
        pygame.draw.rect(surf, color, (8, 8, 24, 8))
        pygame.draw.rect(surf, color, (4, 16, 32, 8))
        pygame.draw.rect(surf, color, (0, 24, 40, 6))
        pygame.draw.rect(surf, WHITE, (12, 12, 4, 4))
        pygame.draw.rect(surf, WHITE, (24, 12, 4, 4))
        return surf

    def update(self, direction):
        self.rect.x += ENEMY_SPEED * direction

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = random.choice([1, 2])
        self.color = (255, 255, 255, random.randint(100, 200))
        self.speed = random.uniform(0.2, 0.7)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def create_enemies():
    enemies = pygame.sprite.Group()
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = 80 + col * 80
            y = 50 + row * 60
            color = ENEMY_COLORS[(row + col) % len(ENEMY_COLORS)]
            enemy = Enemy(x, y, color)
            enemies.add(enemy)
    return enemies

def draw_text(screen, text, size, x, y, color=WHITE, center=True):
    font = pygame.font.SysFont(FONT_NAME, size, bold=True)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = create_enemies()
    stars = [Star() for _ in range(80)]

    enemy_direction = 1
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        player.speed = -PLAYER_SPEED
                    elif event.key == pygame.K_RIGHT:
                        player.speed = PLAYER_SPEED
                    elif event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        bullets.add(bullet)
                else:
                    if event.key == pygame.K_r:
                        # リスタート
                        player = Player()
                        player_group = pygame.sprite.Group(player)
                        bullets = pygame.sprite.Group()
                        enemies = create_enemies()
                        score = 0
                        game_over = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.speed = 0

        if not game_over:
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
            score += len(hits) * 100

            # ゲームオーバー判定
            for enemy in enemies:
                if enemy.rect.bottom >= player.rect.top:
                    game_over = True
            if len(enemies) == 0:
                game_over = True

        # 背景描画
        screen.fill(BLACK)
        for star in stars:
            star.update()
            star.draw(screen)

        # 描画
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        draw_text(screen, f"SCORE: {score}", 28, 120, 20, YELLOW, center=False)

        if game_over:
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//2-40, RED)
            draw_text(screen, "Press R to Restart", 32, SCREEN_WIDTH//2, SCREEN_HEIGHT//2+30, WHITE)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main() 