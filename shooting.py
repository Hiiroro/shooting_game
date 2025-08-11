import pygame
import random
import sys

# 初期化
pygame.init()
WIDTH, HEIGHT = 480, 640
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("シューティング")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

def load_and_scale(path, size):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

PLAYER_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)

player_img = load_and_scale("player.png", PLAYER_SIZE)
enemy_img = load_and_scale("enemy.png", ENEMY_SIZE)

# プレイヤー
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, PLAYER_SIZE[0], PLAYER_SIZE[1])
        self.hp = 3
        self.speed = 5
        self.invincible_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, win):
        if self.invincible_timer == 0:
            win.blit(player_img, self.rect)
        else:
            img = player_img.copy()
            img.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
            win.blit(img, self.rect)    

    def take_damage(self):
        if self.invincible_timer == 0:
            self.hp -= 1
            self.invincible_timer = 60

player = Player()

# 弾・敵
bullets = []
class Enemy:
    def __init__(self, x, y, hp=2):
        self.rect = enemy_img.get_rect(topleft=(x, y))
        self.hp = hp
        self.hit_flash_timer = 0

    def move(self):
        self.rect.y += 3

    def draw(self, win):
        if self.hit_flash_timer > 0:
            img = enemy_img.copy()
            img.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_ADD)
            win.blit(img, self.rect)
            self.hit_flash_timer -= 1
        else:
            win.blit(enemy_img, self.rect)

    def take_damage(self):
        self.hp -= 1
        self.hit_flash_timer = 5

enemies = []

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_img.get_width())
    enemies.append(Enemy(x, -enemy_img.get_height()))
# スコア・ミスカウント
score = 0
missed = 0

# メインループ
running = True
while running:
    clock.tick(60)
    win.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 入力処理
    keys = pygame.key.get_pressed()
    player.move(keys)
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        # 弾は四角形のRectで管理
        bullet_rect = pygame.Rect(player.rect.centerx - 5, player.rect.top, 10, 20)
        bullets.append(bullet_rect)

    # 弾移動
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # 敵生成
    if random.random() < 0.02:
        spawn_enemy()

    # 敵移動と地面到達判定
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw(win)
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)
            missed += 1

    # 弾と敵の当たり判定
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemy.take_damage()
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    score += 1
                break

    # 敵と自機の当たり判定
    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            player.take_damage()
            enemies.remove(enemy)

    if player.invincible_timer > 0:
        player.invincible_timer -= 1

    # ゲームオーバー判定
    if player.hp <= 0 or missed >= 3:
        gameover_text = font.render("GAME OVER", True, (255, 0, 0))
        win.blit(gameover_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    # 描画
    player.draw(win)
    for bullet in bullets:
        pygame.draw.rect(win, (255, 255, 0), bullet)

    # 情報表示
    hp_text = font.render(f"HP: {player.hp}", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    miss_text = font.render(f"Missed: {missed}/3", True, (255, 100, 100))
    win.blit(hp_text, (10, 10))
    win.blit(score_text, (10, 40))
    win.blit(miss_text, (10, 70))

    pygame.display.update()

pygame.quit()
sys.exit()
