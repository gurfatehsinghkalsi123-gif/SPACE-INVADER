import pygame
import random
import math

pygame.init()
pygame.mixer.init()   # <-- SOUND ENGINE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# -------------------------
# LOAD SOUNDS
# -------------------------
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Background music (optional)
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)   # loop forever

# -------------------------
# GRAPHICS
# -------------------------
background = pygame.image.load("background.png")
playerImg = pygame.image.load("player.png")
enemyImg = pygame.image.load("enemy.png")
bulletImg = pygame.image.load("bullet.png")

# -------------------------
# PLAYER
# -------------------------
playerX = 370
playerY = 420
playerX_change = 0

# -------------------------
# ENEMY
# -------------------------
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# -------------------------
# BULLET
# -------------------------
bulletX = 0
bulletY = 420
bulletY_change = 10
bullet_state = "ready"

# -------------------------
# SCORE
# -------------------------
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

def show_score():
    text = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(text, (10,10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx)**2 + (ey - by)**2)
    return distance < 27

# -------------------------
# GAME LOOP
# -------------------------
running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- SHOOT SOUND HERE --------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shoot_sound.play()      # <-- SHOOT SOUND
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerX -= 5
    if keys[pygame.K_RIGHT]:
        playerX += 5

    playerX = max(0, min(playerX, 736))

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # -------- EXPLOSION SOUND HERE --------
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound.play()    # <-- HIT SOUND
            bulletY = 420
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i])

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = 420
        bullet_state = "ready"

    player(playerX, playerY)
    show_score()
    pygame.display.update()

pygame.quit()
