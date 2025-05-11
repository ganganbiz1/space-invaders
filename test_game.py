import pytest
import pygame
from main import Player, Bullet, Enemy, create_enemies, SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_ROWS, ENEMY_COLS

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

def test_player_movement():
    player = Player()
    # 左端まで移動
    player.rect.x = 0
    player.speed = -5
    player.update()
    assert player.rect.left == 0
    # 右端まで移動
    player.rect.x = SCREEN_WIDTH - player.rect.width
    player.speed = 5
    player.update()
    assert player.rect.right == SCREEN_WIDTH

def test_bullet_movement():
    bullet = Bullet(100, 100)
    initial_y = bullet.rect.y
    bullet.update()
    assert bullet.rect.y < initial_y

def test_enemy_creation():
    enemies = create_enemies()
    assert len(enemies) == ENEMY_ROWS * ENEMY_COLS
    for enemy in enemies:
        assert isinstance(enemy, Enemy) 