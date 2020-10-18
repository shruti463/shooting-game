import pygame
import random
import math
from pygame import mixer
pygame.init()


#create screen
screen_height=600
screen_width=800
screen=pygame.display.set_mode((screen_width, screen_height))

#caption
pygame.display.set_caption("SHOOT! SHOOT! SHOOOOOOT!")

#background image
background=pygame.image.load('PERFECT.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)


#create player
player_img=pygame.image.load('people.png')
playerX=350
playerY=480
playerX_change=0


#create enemy
enemy_image=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change =[]
num_of_enemies=8


for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)



#create bullet
bullet_img=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#score
score=0
font= pygame.font.Font('freesansbold.ttf', 36)
textX= 10
textY= 10

#game over text
game_over_font=pygame.font.Font('freesansbold.ttf',64)


#player function
def player(x,y):
    screen.blit(player_img,(x,y))

#enemy function
def enemy(x,y):
    screen.blit(enemy_image[i], (x,y))

#bullet function
def bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+89,y-25))

#collision detection
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance=math.sqrt((math.pow(enemyX - bulletX,2))+(math.pow(enemyY-bulletY,2)))

    if distance<=30:
        return True
    else:
        return False


#score function
def show_score(x,y):
    #rnder means to draw up img of font taxt
    score_value=font.render("Score: " +str(score),True ,(0,0,0))
    screen.blit(score_value,(x,y) )



#game over function
def game_over_text():
    game_over_text=game_over_font.render("GAME OVER!" ,True,(0,0,0))
    screen.blit(game_over_text,(200,250))



#main loop
running =True
while running:
     #BACKGROUND IMAGE
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-10
            if event.key==pygame.K_RIGHT:
                playerX_change=10
            if event.key==pygame.K_SPACE:
                if bullet_state =="ready":
                    #to load the sound effect
                    bullet_sound=mixer.Sound('laser.wav')
                    #to play the sound effect
                    bullet_sound.play()

                    bulletX=playerX
                    bullet(bulletX, bulletY)


        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT  or  event.key==pygame.K_RIGHT:
                playerX_change=0

    #player movement
    playerX +=playerX_change

    #check for boundaries
    if playerX<=0:
        playerX=0
    elif playerX>=670:
        playerX=670

    #enemy movement
    for i in range(num_of_enemies):
        if enemyY[i]>470:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] =3
            enemyY[i]+= enemyY_change[i]

        elif enemyX[i] >=750:
            enemyX_change[i] =-3
            enemyY[i]+= enemyY_change[i]

        #collision detection
        collision=iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score+=1

            #respawn the enemy
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i], enemyY[i])
    #bullet movement

    if bulletY<=0:
         bulletY=480
         bullet_state="ready"
    if bullet_state =="fire":
        bullet(bulletX,bulletY)
        bulletY -=bulletY_change


    #player
    player(playerX, playerY)
    show_score(textX, textY)
    #update the screen
    pygame.display.update()



pygame.quit()

