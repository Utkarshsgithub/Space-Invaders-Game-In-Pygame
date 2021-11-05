import pygame
import random
import math
from pygame import mixer

pygame.init()

# Window Size
screen = pygame.display.set_mode((800, 600))

# Game Title
pygame.display.set_caption("Space Invaders")

# Game Icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background
bgs = ["background1.png"]
background = pygame.image.load(random.choice(bgs))

# Background Music
mscs = ["bgmusic1.wav"]
mixer.music.load(random.choice(mscs))
mixer.music.play(-1)
mixer.music.set_volume(0.5)

# Player
plyrs = ["spaceship1.png", "spaceship2.png", "spaceship3.png"]
player_choice = random.choice(plyrs)
playerImg = pygame.image.load(player_choice)

playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enms = ["enemy1.png", "enemy2.png", "enemy3.png"]
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

no_of_enemies = 10

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load(random.choice(enms)))

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
blts = ["bullet1.png"]
bulletImg = pygame.image.load(random.choice(blts))

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Score
score_value = 0
fonts = ["font1.otf"]
font = pygame.font.Font(random.choice(fonts), 30)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font(random.choice(fonts), 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))


def check_collision(enemyX, enemyY, bulletX, bulletY):
    # search on Google "Distance between two objects coordinates" and you'll get this formula
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:

    # RGB
    screen.fill((0, 0, 0))

    # BG Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change -= 0.9

            if event.key == pygame.K_RIGHT:
                playerX_change += 0.9

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("shoot.wav")
                    mixer.Sound.play(bullet_sound)
                    # Get the position of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player Movement

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    for i in range(no_of_enemies):

        if enemyY[i] > 440:

            for j in range(no_of_enemies):
                over_sound = mixer.Sound("gameover.wav")
                mixer.Sound.play(over_sound)
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision

        collision = check_collision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            collision_sound = mixer.Sound("shot.wav")
            mixer.Sound.play(collision_sound)
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
