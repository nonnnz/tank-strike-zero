import pygame
import math
import random
import csv


from pygame.constants import KEYDOWN, K_f

pygame.init()

"""
Setting
"""
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tank Strike')
icon = pygame.image.load("public/icon.ico")
pygame.display.set_icon(icon)

background = pygame.image.load("public/images/map.png")
"""
PLAYER
"""


psize = 128

pimg = pygame.image.load("public/images/tank-main.png")
px = 100  # start X
py = HEIGHT - psize  # start Y
pxchange = 0
pspeed = 0


def player(x, y):
    screen.blit(pimg, (x, y))


"""
ENEMY
"""

esize = 64

eimg = pygame.image.load("public/images/Pumpkill-3.png")
ex = 50
ey = 0
eychange = 1


def enemy(x, y):
    screen.blit(eimg, (x, y))


"""
MULTI-ENEMY
"""
exlist = []
eylist = []
ey_change_list = []  # enemy speed
allenemy = 3

for i in range(allenemy):
    exlist.append(random.randint(50, WIDTH - esize))
    eylist.append(random.randint(0, 100))
    # ey_change_list.append(random.randint(1, 2))  # สุ่มความเร็ว enemy
    ey_change_list.append(1)  # เพิ่มความเร็วหลังจากยิงโดน
"""
fire
"""
# 3 - mask - mask.png
msize = 32
mimg = pygame.image.load("public/images/Exhaust_Fire.png")
mx = 100
my = HEIGHT - psize
mychange = 20
mstate = 'ready'


def fire_mask(x, y):
    global mstate
    mstate = 'fire'
    screen.blit(mimg, (x, y))

"""
CLASS EXPLOSION (new edit)
"""
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,9):
            img = pygame.image.load(f"public/images/Explosion_{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        explosion_speed = 4
        # update animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # reset index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()

"""
COLLISION
"""


def is_conllision(ecx, ecy, mcx, mcy):
    # เช็คการชน
    distance = math.sqrt(math.pow(ecx - mcx, 2) + math.pow(ecy - mcy, 2))

    if distance < (esize / 2) + (msize / 2):
        # ระยะที่ชนกัน
        return True
    else:
        return False


"""
SCORE
"""
allscore = 0
font = pygame.font.Font("public/font/Kanit-Bold.ttf", 36)


def showscore():
    score = font.render(f'คะแนน: {allscore} คะแนน', True, (255, 255, 255))
    screen.blit(score, (30, 30))

def score_reset():
    with open('score.csv', mode='w') as csv_file:
        score_del = csv.writer(csv_file)
        score_del.writerow(['0'])

"""
SCORE HIGHEST
"""
highest_score = 0
fontscore = pygame.font.Font("public/font/Kanit-Light.ttf", 30)

def read_highestscore():
    global highest_score
    with open(r'score.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row:
                highest_score = int(row[0])


read_highestscore()

def highest():
    scoretext = fontscore.render(f'คะแนนสูงสุด {highest_score}', True, (0, 255, 0))
    screen.blit(scoretext, (30, 70))


"""
BOOST
"""
asize = 64

aimg = pygame.image.load("public/images/booster.png")
ax = 50
ay = 0
aychange = 1


def BOOSTER(x, y):
    screen.blit(aimg, (x, y))



"""
STATS
"""
hsize = 32
himg = pygame.image.load("public/images/full_heart.png")
hx = WIDTH  - hsize
hy = 10
max_heart = 3
allheart = max_heart



def heart(x, y):
    screen.blit(himg, (x, y))


"""
SOUND
"""
pygame.mixer.music.load("public/sounds/oldvideogame.wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

firesound = pygame.mixer.Sound("public/sounds/Shoot.wav")
firesound.set_volume(0.2)
esound = pygame.mixer.Sound("public/sounds/roblox_death_sound_effect.ogg")
esound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound("public/sounds/Explosion 11 (1).wav")
explosion_sound.set_volume(0.6)
gameoversound = pygame.mixer.Sound("public/sounds/Failed.ogg")
asound = pygame.mixer.Sound("public/sounds/Minecraft_Glass_Break.ogg")
asound.set_volume(0.2)
"""
GAME OVER
"""
gamevoer_bg = pygame.image.load("public/images/gameover.png")
fontover = pygame.font.Font('angsana.ttc', 80)
fontnew = pygame.font.Font('angsana.ttc', 20)
playsound = False
gameover = False


def game_over():
    global playsound
    global gameover
    if playsound == False:
        gameoversound.play()
        playsound = True
    if gameover == False:
        gameover = True


"""
GAME LOOP
"""

# intro 

intro = True

alpha = 0

while intro:
    background_intro = pygame.image.load("public/images/intro-bg.png")
    logo = pygame.image.load("public/images/intro-logo.png")

    alpha_vel = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # press enter to start
                intro = False
    # draw logo

    if alpha < 255:
        j = 0
        screen.blit(background_intro, (0, 0))
        pygame.display.update()
        pygame.time.delay(1000)
        while j < 255:
            j += 1
            logo.set_alpha(j)
            screen.blit(logo,(0,0))
            pygame.display.flip()
            if j >= 50:
                j += 50
            pygame.time.delay(20)
            alpha += j
            print(j)
    

running = True

clock = pygame.time.Clock()
FPS = 60
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pxchange = -10 - pspeed
            if event.key == pygame.K_RIGHT:
                pxchange = 10 + pspeed

            if event.key == pygame.K_SPACE:
                if mstate == 'ready':
                    firesound.play()
                    mx = px + (psize / 2) - 13 # ขยับ
                    fire_mask(mx, my)

            if event.key == pygame.K_r:
                score_reset()
                read_highestscore()

            if event.key == pygame.K_n:
                gameover = False
                playsound = False
                allscore = 0
                allheart = max_heart
                hx2 = hx - hsize
                hx3 = hx2 - hsize
                hx = WIDTH - hsize
                pygame.mixer.music.play(-1)
                read_highestscore()
                # reset enemy speed
                for j in range(0, 3):
                    ey_change_list[j] = 1
                # reset enemy
                for i in range(allenemy):
                    eylist[i] = random.randint(0, 100)
                    exlist[i] = random.randint(50, WIDTH - psize)

        if event.type == pygame.KEYUP: # เมื่อไม่กด
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pxchange = 0

    #draw explosion
    explosion_group.draw(screen)
    explosion_group.update()



    """
    RUN PLAYER 
    """
    player(px, py)

    if px <= 0:
        px = 0
        px += pxchange
    elif px >= WIDTH - psize:
        px = WIDTH - psize
        px += pxchange
    else:
        px += pxchange

    """
    RUN ENEMY
    """
    '''
    enemy(ex, ey)
    ey += eychange
    # ชนพื้น
    if ey == HEIGHT:
        ey = 0
        ex = random.randint(50, WIDTH - esize)
    '''


    """
    BOOSTER DROP
    """
    BOOSTER(ax, ay)
    ay += aychange
    applecollisionmulit = is_conllision(ax, ay, mx, my)

    if applecollisionmulit:
        asound.play()
        ay = 0
        ax = random.randint(50, WIDTH - esize)
        if allheart < max_heart:
            allheart += 1
        if pspeed < 5:
            pspeed += 1
    # ชนพื้น
    if ay == HEIGHT:
        ay = 0
        ax = random.randint(50, WIDTH - asize)

    if allheart == 0:
        ay = -asize
        pspeed = 0



    """
    RUN MULTI ENEMY
    """
    damage = 0
    for i in range(allenemy):
        # เพิ่ม enemy speed
        if eylist[i] > HEIGHT - esize and gameover == False:
            eylist[i] = 0
            allheart -= 1
            #print(allheart)
            if allheart <= 0:
                if allscore > highest_score:
                    with open('score.csv', mode='w') as csv_file:
                        score_writer = csv.writer(csv_file)
                        score_writer.writerow([allscore])
                game_over()
                pygame.mixer.music.stop()
                for i in range(allenemy):
                    eylist[i] = 1000
                break
        if gameover == True:
            screen.blit(gamevoer_bg, (0, 0))
            # overtext = fontover.render('GAME OVER', True, (255, 0, 0))
            # screen.blit(overtext, (300, 300))
            # overtext2 = fontnew.render('pass [N] new game', True, (255, 255, 255))


        eylist[i] += ey_change_list[i]
        collisionmulit = is_conllision(exlist[i], eylist[i], mx, my)
        if collisionmulit:
            my = HEIGHT - psize
            mstate = 'ready'
            explosion = Explosion(exlist[i], eylist[i]) # explosion
            eylist[i] = 0
            exlist[i] = random.randint(50, WIDTH - esize)
            allscore += 1
            ey_change_list[i] += 1
            explosion_sound.play()
            esound.play()
            explosion_group.add(explosion)  # explosion

        enemy(exlist[i], eylist[i])

        # ระบบเลือด
        hx2 = hx - hsize
        hy2 = hy
        hx3 = hx2 - hsize
        hy3 = hy
        if allheart <= 1:
            hx2 = -1000
        if allheart <= 2:
            hx3 = -1000
        if allheart == 0:
            hx = -1000
        heart(hx, hy)
        heart(hx2, hy2)
        heart(hx3, hy3)
        # ชนพื้น
        '''
        if eylist[i] == HEIGHT:
            eylist[i] = 0
            exlist[i] = random.randint(50, WIDTH - esize)
        '''
    """
    FIRE
    """
    if mstate == 'fire':
        fire_mask(mx, my)
        my = my - mychange
    # เช็คว่าชนยัง
    if my <= 0:
        my = HEIGHT - psize
        mstate = 'ready'
    # เช็คว่าชนหรือไม่
    collision = is_conllision(ex, ey, mx, my)
    if collision:
        my = HEIGHT - psize
        mstate = 'ready'
        ey = 0
        ex = random.randint(50, WIDTH - esize)
        allscore += 1
        # สุ่มตำแหน่ง ความกว้างหน้าจอ - ขนาด virus
    showscore()
    highest()
    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(FPS)