import pygame
from pygame import mixer
import random
import math


# initialization
pygame.init()

# screen displayer
screen = pygame.display.set_mode((800, 600))
# background image
background = pygame.image.load("5426839.jpg")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title
pygame.display.set_caption("newGame")
# icon
icon = pygame.image.load("free-icon-spaceship-985191.png")
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load("free-icon-spaceship_1.png")
playerX = 370
playerY = 480
playerX_moving = 0

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):

    enemyImg.append(pygame.image.load('spaceship.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
# the bullet in screen
# ready-> bullet is currently in screen
# fire -> the bullet  is currently moving
bulletImg = pygame.image.load("balle.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX= 10
textY = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, x))
def game_over_text():
    over_text = over_font.render("Game Over", True, (0, 255, 255))
    screen.blit(over_text, (200, 255))

def play(x, y):
    screen.blit(playerImg, (x, y))



def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False



# loop
running = True
while running:
    # background color
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    # movement
    # playerY -=0.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_moving = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_moving = 0.5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                # only fire the bullet if it is in the "ready" state
                if bullet_state == "ready":
                    fire_bullet(playerX, bulletY)
                    bulletX = playerX

        # check if a key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_moving = 0

    playerX += playerX_moving
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    # enemy movement

    for i in range(num_of_enemy):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 740:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i]= random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)


    play(playerX, playerY)
    show_score(textX, textY)


    pygame.display.update()
