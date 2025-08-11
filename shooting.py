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

# プレイヤー
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)
        self.hp = 3
        self.speed = 5
        self.invincible_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, win):
        color = (0, 200, 255) if self.invincible_timer == 0 else (150, 150, 255)
        pygame.draw.rect(win, color, self.rect)

    def take_damage(self):
        if self.invincible_timer == 0:
            self.hp -= 1
            self.invincible_timer = 60

player = Player()

# 弾・敵
bullets = []
class Enemy:
    def __init__(self, x, y, hp=2):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.hp = hp
        self.hit_flash_timer = 0

    def move(self):
        self.rect.y += 3

    def draw(self, win):
        color = (255, 100, 100) if self.hit_flash_timer == 0 else (255, 255, 255)
        pygame.draw.rect(win, color, self.rect)
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

    def take_damage(self):
        self.hp -= 1
        self.hit_flash_timer = 3

enemies = []

def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    enemies.append(Enemy(x, -40))

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
        bullet = pygame.Rect(player.rect.centerx - 5, player.rect.top, 10, 20)
        bullets.append(bullet)

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
